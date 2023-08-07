#!/usr/bin/python
# -*- coding: UTF-8 -*-
import collections
import getopt
import os
import shutil
import sys
import zipfile
from collections import OrderedDict

import requests
import xlrd
import yaml

default_sheets = ['info', 'projects', 'config', 'scheduler', 'trigger']
HEADERS = {'Content-Type': 'application/x-www-form-urlencoded', 'X-Requested-With': 'XMLHttpRequest'}


def ordered_yaml_load(yaml_path, Loader=yaml.Loader, object_pairs_hook=OrderedDict):
    class OrderedLoader(Loader):
        pass

    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return object_pairs_hook(loader.construct_pairs(node))

    OrderedLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_mapping)
    with open(yaml_path) as stream:
        return yaml.load(stream, OrderedLoader)


def ordered_yaml_dump(data, stream=None, Dumper=yaml.SafeDumper, **kwds):
    class OrderedDumper(Dumper):
        pass

    def _dict_representer(dumper, data):
        return dumper.represent_mapping(
            yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
            data.items())

    OrderedDumper.add_representer(OrderedDict, _dict_representer)
    return yaml.dump(data, stream, OrderedDumper, **kwds)


'''
 check dependency jobs whether exits in above jobs or not
'''


def check_job(flow, depend_jobs):
    exists_jobs = []
    for job in flow['nodes']:
        exists_jobs.append(job.get('name'))
    return set(depend_jobs).issubset(exists_jobs)


'''
check some cell value whether is null or not
'''


def null(var, desc):
    if len(var.strip()) == 0:
        raise Exception('The value ' + desc + 'is required')


'''
parse jobs and flows from excel 
'''


def parse_flows(excel, sheet_name):
    flow_list = collections.OrderedDict()
    sheet1 = excel.sheet_by_name(sheet_name)
    for i in range(1, sheet1.nrows):
        line = sheet1.row_values(i)
        if len(line) == 0:
            pass
        # get a flow from flow_list
        flow = flow_list.get(line[1], collections.OrderedDict())
        config = parse_flow_config(sheet_name, flow, i, line)
        if config:
            flow['config'] = config

        nodes = flow.get('nodes', [])
        job = parse_job(flow, line)
        nodes.append(job)
        flow['nodes'] = nodes

        flow_list[line[1]] = flow
    return flow_list


'''
    parse flow config from excel column
'''


def parse_flow_config(sheet_name, flow, i, line):
    config = flow.get('config', collections.OrderedDict())
    if len(config) != 0:
        return config
    if line[3]:
        for conf in line[3].strip().split('|'):
            cp = conf.strip().split('=')
            if not cp:
                pass
            try:
                config[cp[0]] = cp[1]
            except IndexError:
                print('location the sheet_name: %s the %d  line  has error' % (sheet_name, i + 1))
                print("flow configs error:", i + 1, line[3])

    else:
        print('Please set the config at first row[%s->%d] of the flow!' % (sheet_name, i + 1))
    return config


'''
parse jobs config from excel column
'''


def parse_job(flow, line):
    job_name, job_type = check_null(line)
    job = collections.OrderedDict()
    job['name'] = job_name
    job['type'] = job_type
    depend_jobs = []
    if line[8] and line[8].strip() != '':
        depend_jobs = line[8].strip().split('|')
    if len(depend_jobs) != 0:
        job['dependsOn'] = depend_jobs
        if not check_job(flow, depend_jobs):
            raise Exception(
                'job ' + line[1] + '\'s depends: ' + line[8] + ' On not exist in above jobs')
    job_config = {'command': line[7]}
    job['config'] = job_config
    return job


'''
check null parameter from excel column
'''


def check_null(line):
    job_name = line[4].strip()
    null(job_name, 'job_name')
    job_type = line[6].strip()
    null(job_type, 'job_type')
    return job_name, job_type


def handle_dir(base_dir, sheet_name):
    try:
        shutil.rmtree(base_dir)
    except FileNotFoundError:
        pass
    os.mkdir(base_dir)
    # generate azkaban version describe file
    with open(base_dir + os.sep + sheet_name + '.project', 'w', encoding='utf-8') as version_file:
        version_file.write('azkaban-flow-version: 2.0')
        version_file.close()


'''
compress project's all files to zipfile and save it to base_dir
'''


def make_zip(projects, base_dir):
    for project in projects:
        source_dir = base_dir + os.sep + project
        zips = zipfile.ZipFile(source_dir + '.zip', 'w')
        pre_len = len(os.path.dirname(source_dir))
        for parent, dirnames, filenames in os.walk(source_dir):
            for filename in filenames:
                pathfile = os.path.join(parent, filename)
                arcname = pathfile[pre_len:].strip(os.path.sep)
                zips.write(pathfile, arcname)
            print('compress %s successfully!' % source_dir)
        zips.close()


'''
you can choose either schedule  or trigger,not both of them 
'''


def check_schedule_trigger(excel):
    # 1 打开scheduler页，获取所有project-->flow_name的map
    ss = excel.sheet_by_name('scheduler')
    st = excel.sheet_by_name('trigger')
    s_map = {}
    for i in range(1, ss.nrows):
        rv = ss.row_values(i)
        if rv[3] == 1 and rv[1] != '' and rv[0] != '':
            k = rv[0] + rv[1]
            v = chr(66) + str(i + 1)
            if s_map.get(k):
                raise Exception('Duplicate workflow in scheduler: %s value: %s' % (v, rv[0] + '-' + rv[1]))
            else:
                s_map[k] = v
    # 2 打开trigger页，获取所有project-->flow_name的map，check dep_name是否冲突，将冲突的部分坐标返回
    for i in range(1, st.nrows):
        rv = st.row_values(i)
        if rv[0] == 1 and rv[1] != '' and rv[2] != '':
            k1 = rv[1] + rv[2]
            v1 = chr(67) + str(i + 1)
            try:
                if s_map[k1]:
                    raise Exception('scheduler-->%s conflict with trigger-->%s  project flow: %s' % (s_map[k1], v1, k1))
            except KeyError:
                pass


'''
add trigger for some workflow by configuration in sheet named "trigger" 
'''


def add_triggers(flows, excel, project):
    trigger_sheet_name = 'trigger'
    ts = excel.sheet_by_name(trigger_sheet_name)
    # flows.get('trigger', collections.OrderedDict())
    project_name = 'default'
    dep_list = {}
    for i in range(1, ts.nrows):
        rv = ts.row_values(i)
        enable = rv[0]
        project_name = rv[1]
        flow_name = rv[2]
        if enable == 1 and project_name == project and flow_name != "":
            flow = flows.get(flow_name)
            if not flow:
                pass
            trigger = flow.get('trigger', collections.OrderedDict())
            max_min = 1440
            if rv[4]:
                max_min = int(rv[4])
            trigger['maxWaitMins'] = max_min

            schedule_1 = trigger.get('schedule', collections.OrderedDict())
            schedule_1['type'] = 'cron'
            cron = "0 10 * * * ?"
            if rv[3]:
                cron = rv[3]
            schedule_1['value'] = cron
            trigger['schedule'] = schedule_1

            deps = trigger.get('triggerDependencies', [])
            dep = collections.OrderedDict()
            params = collections.OrderedDict()
            k = project_name + flow_name

            dl = dep_list.get(k, [])
            if dl.__contains__(rv[5]):
                raise Exception("duplicate dependency:\n%d %s\n%d %s" % (i, ts.row_values(i - 1), i+1, rv))
            else:
                dl.append(rv[5])
                dep_list[k] = dl
            dep['name'] = rv[5]
            dep['type'] = rv[6]
            params['match'] = rv[7]
            params['topic'] = rv[8]
            dep['params'] = params
            deps.append(dep)

            trigger['triggerDependencies'] = deps
            flow['trigger'] = trigger
            flows[flow_name] = flow

    return flows


'''
generate all flows file in base directory 
'''


def generator(excel, flow_sheets, save_dir):
    # check trigger and schedule conflict
    check_schedule_trigger(excel)
    for project in flow_sheets:
        flows = parse_flows(excel, project)
        flows = add_triggers(flows, excel, project)
        project_dir = save_dir + os.sep + project
        handle_dir(project_dir, project)
        for f in flows:
            flow_file = project_dir + os.sep + f + '.flow'
            with open(flow_file, 'w', encoding='utf-8') as f_file:
                ordered_yaml_dump(flows[f], f_file)
                f_file.close()
        print(project_dir + '.zip is generated')


'''
Login Azkaban Server return a Session
'''


def login(url, username, password):
    session = requests.Session()
    data = {
        'action': 'login',
        'username': username,
        'password': password
    }
    response = session.post(url, data=data, verify=False, headers=HEADERS)
    if response.raise_for_status():
        raise Exception("login azkaban failed,please check the config sheet's content")
    else:
        return session


'''
create enabled project on Azkaban Server
'''


def create_project(excel, url, session):
    ps = excel.sheet_by_name('projects')
    p_ids = {}
    for r in range(1, ps.nrows):
        p_name = ps.cell_value(r, 1)
        enable = ps.cell_value(r, 0)
        if (not enable) or p_name == '':
            continue
        p_desc = ps.cell_value(r, 2)
        if p_desc == '':
            p_desc = p_name
        params = (
            ('action', 'create'),
        )
        data = {
            'name': p_name,
            'description': p_desc
        }
        response = session.post(url + 'manager', data=data, params=params, verify=False, headers=HEADERS)
        if response.raise_for_status():
            raise Exception("request failed")
        else:
            print("%s-->%s :%s" % (p_name, p_desc, response.json()))
        p_ids[p_name] = fetch_projects_id(url, session, p_name)
    print("============create project Successfully!============")
    return p_ids


def schedule_flow(url, session, p_name, f_name, cron):
    headers = {
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
    }

    data = {
        'project': p_name,
        'ajax': 'scheduleCronFlow',
        'flow': f_name,
        'disabled': '[]',
        'failureEmailsOverride': 'false',
        'successEmailsOverride': 'false',
        'failureAction': 'finishCurrent',
        'failureEmails': '',
        'successEmails': '',
        'notifyFailureFirst': 'false',
        'notifyFailureLast': 'false',
        'concurrentOption': 'skip',
        'projectName': p_name,
        'cronExpression': cron
    }

    response = session.post(url + 'schedule', headers=headers, data=data, verify=False)
    if response.raise_for_status():
        raise Exception("request failed")
    else:
        print(response.json())
        return response.json()['scheduleId']


def remove_schedule(url, session, schedule_id):
    data = {
        'action': 'removeSched',
        'scheduleId': schedule_id
    }
    response = session.post(url + 'schedule', headers=HEADERS, data=data, verify=False)
    if response.raise_for_status():
        raise Exception("request failed")
    else:
        print(response.json())


'''
get project_id by project_name
'''


def fetch_projects_id(url, session, project_name):
    params = {
        'project': project_name,
        'ajax': 'fetchprojectflows'
    }
    response = session.get(url + 'manager', headers=HEADERS, params=params, verify=False)
    project_id = response.json().get('projectId')
    if response.raise_for_status():
        raise Exception("request failed")
    else:
        if project_id:
            print('project %s id is: %s' % (project_name, project_id))
            return project_id


def fetch_schedule_id(url, session, project_id, flow_name):
    params = {
        'ajax': 'fetchSchedule',
        'projectId': project_id,
        'flowId': flow_name
    }

    response = session.get(url + 'schedule', headers=HEADERS, params=params, verify=False)
    if response.raise_for_status():
        raise Exception("request failed")
    else:
        if response.json():
            return response.json()['schedule']['scheduleId']
    return None


'''
set a sla for a scheduled flow ,which configuration at scheduler sheet,kill or send email is required
'''


def set_sla(url, session, schedule_id, sla_emails, s):
    email_switch, kill_switch = 'false', 'false'
    if s[3].value:
        email_switch = 'true'
    if s[4].value:
        kill_switch = 'true'
    sets = s[0].value + ',' + s[1].value + ',' + s[2].value + ',' + email_switch + ',' + kill_switch
    params = {
        'ajax': 'setSla',
        'slaEmails': sla_emails,
        'scheduleId': schedule_id,
        'settings[0]': sets
    }
    response = session.post(url + 'schedule', params=params, headers=HEADERS, verify=False)
    if response:
        print("set sla for scheduleId ", response.json(), schedule_id)


'''
Which flow was scheduled must be enable in scheduler and the owner of the flow must be enable also.
'''


def schedule(excel, url, session, maps):
    schedule_sheet = excel.sheet_by_name('scheduler')
    for row in range(1, schedule_sheet.nrows):
        project_name = schedule_sheet.cell_value(row, 1).strip()
        flow_name = schedule_sheet.cell_value(row, 2).strip()
        cron = schedule_sheet.cell_value(row, 3).strip()
        enable = schedule_sheet.cell_value(row, 0)
        if project_name == '' or flow_name == '':
            continue
        if project_name and flow_name:
            if cron != '' and enable and maps.get(project_name, None):
                sla_enable = schedule_sheet.cell_value(row, 7)
                schedule_id = schedule_flow(url, session, project_name, flow_name, cron)
                if sla_enable:
                    emails = schedule_sheet.cell_value(row, 8)
                    sla_setting = schedule_sheet.row_slice(row, 9, 14)
                    set_sla(url, session, schedule_id, emails, sla_setting)
            else:
                if maps.get(project_name, None):
                    schedule_id = fetch_schedule_id(url, session, maps[project_name], flow_name)
                    if schedule_id:
                        remove_schedule(url, session, schedule_id)


'''
upload single project to Azkaban Server
'''


def upload_project(url, session, base_dir, project):
    from requests_toolbelt.multipart.encoder import MultipartEncoder
    zip_file_name = project + '.zip'
    zip_path = base_dir + os.sep + zip_file_name
    upload_data = MultipartEncoder(
        fields={
            'ajax': 'upload',
            'project': project,
            'file': (zip_file_name, open(zip_path, 'rb'), 'application/zip')
        }
    )
    response = session.post(url + 'manager', data=upload_data, headers={'Content-Type': upload_data.content_type})
    if response.raise_for_status():
        raise Exception("request failed")
    else:
        print('upload project: %s successfully! success info: %s' % (project, response.json()))


'''
The project must be enabled before create and upload 
In other words ,the project has configure at a single sheet
'''


def run_upload(url, session, projects, b_dir):
    requests.packages.urllib3.disable_warnings()
    for p in projects:
        upload_project(url, session, b_dir, p)


'''
exclude project which enable column is False and default_sheet 
'''


def get_valid_projects(xl):
    all_sheets = xl.sheet_names()
    for default_sheet in default_sheets:
        all_sheets.remove(default_sheet)
    projects_sheet = xl.sheet_by_name('projects')
    for x in range(1, projects_sheet.nrows):
        project_name = projects_sheet.cell_value(x, 0)
        if (not projects_sheet.cell_value(x, 2)) and all_sheets.__contains__(project_name):
            all_sheets.remove(project_name)
    return all_sheets


def usage():
    print('''Usage: azkaban_helper [options] excel_file
    
    Options:
             -g|--generate     generate flows of project,no zip and other operators
             -c|--create       create projects at azkaban
             -u|--upload       upload zip file to azkaban server, it will attempt create project before upload
             -s|--schedule     if you just only want to modify a flows scheduler but not modify flow's content,use it
                excel_file     flow's configuration file must be specified     

             default behavior is executes all the steps above.
          ''')


def handle_args():
    generate_only, create_only, upload_only, schedule_only = False, False, False, False
    excel_file = ''
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hgcus',
                                   ['help', 'generate', 'create', 'upload', 'schedule'])
        for o, a in opts:
            if o in ('-h', '--help'):
                usage()
                sys.exit()
            if o in ('-g', '--generate'):
                generate_only = True
            if o in ('-c', '--create'):
                create_only = True
            if o in ('-u', '--upload'):
                upload_only = True
            if o in ('-s', '--schedule'):
                schedule_only = True
        if not len(args):
            usage()
            print("ERROR: Excel file is Required!!!")
            sys.exit(-1)
        excel_file = args[0]
        if not os.path.exists(excel_file):
            print(excel_file, 'is not exists')
            sys.exit(-2)
    except getopt.GetoptError:
        usage()
    print(
        '========================\n'
        ' generate_only=%s\n create_only  =%s\n upload_only  =%s\n schedule_only=%s\n excel_file   =%s'
        '\n========================'
        % (generate_only, create_only, upload_only, schedule_only, excel_file))

    return generate_only, create_only, upload_only, schedule_only, excel_file


def get_urls_info(excel):
    url_config = excel.sheet_by_name('config')
    urls = []
    for i in range(1, url_config.nrows):
        u_conf = get_login_config(url_config, i)
        if u_conf:
            urls.append(u_conf)
    return urls


'''
from config sheet read azkaban_url,password,username,base_dir
'''


def get_login_config(config_sheet, row_index):
    # only select enable column values is True
    enable = config_sheet.cell_value(row_index, 0)
    if enable != 0:
        url = config_sheet.cell_value(row_index, 1).strip()
        if not url.endswith('/'):
            url = url + '/'
        username = config_sheet.cell_value(row_index, 2).strip()
        password = config_sheet.cell_value(row_index, 3).strip()
        base_dir = config_sheet.cell_value(row_index, 4).strip()

        if not base_dir:
            base_dir = os.getcwd()
        else:
            if base_dir.endswith(os.sep):
                base_dir = base_dir[:-1]
        if not os.path.isdir(base_dir):
            print(base_dir, 'it\'s not exists,auto create it')
            os.mkdir(base_dir)
        return url, username, password, base_dir
    else:
        return None


def main():
    requests.packages.urllib3.disable_warnings()
    # handle args
    generate_only, create_only, upload_only, schedule_only, excel_file = handle_args()
    excel = xlrd.open_workbook(excel_file)
    # get valid sheets
    valid_sheets = get_valid_projects(excel)
    web_configs = get_urls_info(excel)
    generator(excel, valid_sheets, web_configs[0][3])
    print("============generator projects Successfully!============")
    make_zip(valid_sheets, web_configs[0][3])
    print("============compress projects Successfully!============")
    for w in web_configs:
        url, username, password, save_dir = w[0], w[1], w[2], w[3]
        if generate_only:
            sys.exit()
        if create_only:
            session = login(url, username, password)
            create_project(excel, url, session)
            session.close()
            sys.exit()
        if upload_only:
            session = login(url, username, password)
            run_upload(url, session, valid_sheets, save_dir)
            session.close()
            sys.exit()
        if schedule_only:
            session = login(url, username, password)
            pro_map = create_project(excel, url, session)
            schedule(excel, url, session, pro_map)
            session.close()
            sys.exit()

        # The steps below is needed connection to Azkaban Server
        session = login(url, username, password)
        pro_map = create_project(excel, url, session)
        run_upload(url, session, valid_sheets, save_dir)
        print("============upload projects Successfully!============")
        schedule(excel, url, session, pro_map)
        print("============schedule flows Successfully!============")
        session.close()


if __name__ == '__main__':
    main()
