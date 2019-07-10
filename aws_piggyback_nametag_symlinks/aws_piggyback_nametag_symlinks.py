#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-
#####################################
# Name: aws_piggyback_nametag_symlinks
# Version: 1.0-20190702
# Author: Davide Del Grande <delgrande.davide@gmail.com> / <davide.delgrande@lanewan.it>
# Purpose: Analyzes CheckMK AWS Agent piggybacked files and creates shadow symlinks named after Name Tags
#####################################
from __future__ import print_function
import os, sys, posixpath, tempfile
import re, json
import pprint


########################################################################################################
## This is only for CheckMK ver < 1.6 (where the EC2 Tags are already stored as section "ec2_labels")
########################################################################################################
def generate_fake_ec2_labels(instanceid, tagdict):
    try:
        return json.dumps({'Name': tagdict[instanceid]})
    except:
        return {}

########################################################################################################
########################################################################################################

########################################################################################################
## This is only for CheckMK ver < 1.6 (where the EC2 Tags are already stored as section "ec2_labels")
########################################################################################################
class Legacy_AWS_EC2_Tags_Online:
    def __init__(self, regions=[]):
        self.__requested_regions = regions
        self.__timestamp = 0


    def append_omd_to_python_path(self):
        import os,sys
        HOMEDIR = os.getenv('HOME','~')
        HOMEDIR = os.getenv('OMD_ROOT',HOMEDIR)
        LIBDIR = os.path.join(HOMEDIR,'lib/python')
        if LIBDIR not in sys.path:
            sys.path.append(LIBDIR)


    @property
    def regions(self):
        if self.__requested_regions != [] and self.__requested_regions != ['current']:
            return self.__requested_regions

#        if self.__requested_regions == ['current']:
#            try:
#                import requests
#            except:
#                self.append_omd_to_python_path()
#                import requests
#            try:
#                self.__requested_regions = requests.get('http://169.254.169.254/latest/dynamic/instance-identity/document', timeout=1).json()['region'].split()
#            except:
#                self.__requested_regions == []


        elif self.__requested_regions == []:
            try:
                import boto3
            except ImportError:
                self.append_omd_to_python_path()
                import boto3

            self.__requested_regions = boto3.session.Session().get_available_regions('ec2',allow_non_regional=True)

        return self.__requested_regions


    @property
    def ec2tags(self):
        if self.__timestamp != 0:
            return self.__ec2tags
        else:
            try:
                from time import time
                self.__timestamp = time()
            except:
                self.__timestamp = 1

            try:
                from collections import defaultdict
                self.__ec2tags = defaultdict(dict)
            except:
                raise


            try:
                import boto3
            except ImportError:
                self.append_omd_to_python_path()
                import boto3


            for region in self.regions:
                ec2client = boto3.client('ec2', region_name=region)
                response = ec2client.describe_tags(
                    Filters = [
                        {
                        'Name': 'resource-type',
                        'Values': ['instance']
                        },
                        {
                         'Name': 'tag:Name',
                        'Values': ['*']
                        },
                    ]
                )

                for t in response["Tags"]:
                    self.__ec2tags[region][t['ResourceId']] = t['Value']

            return self.__ec2tags


    @ec2tags.setter
    def ectags(self, x):
        self.__ec2tags = self.__ec2tags ## read-only
########################################################################################################
########################################################################################################


########################################################################################################
## This is only for CheckMK ver < 1.6 (where the EC2 Tags are already stored as section "ec2_labels")
########################################################################################################
aws_regions = "eu-west-1".split()
legacy_ec2_tags_online = Legacy_AWS_EC2_Tags_Online(aws_regions)

########################################################################################################
########################################################################################################

_os_alt_seps = list(sep for sep in [os.path.sep, os.path.altsep]
                    if sep not in (None, '/'))

def safe_join(directory, filename): ## taken from: https://github.com/pallets/flask/blob/50dc2403526c5c5c67577767b05eb81e8fab0877/flask/helpers.py#L633
    """Safely join `directory` and `filename`.

    Example usage::

    @app.route('/wiki/<path:filename>')
    def wiki_page(filename):
    filename = safe_join(app.config['WIKI_FOLDER'], filename)
    with open(filename, 'rb') as fd:
    content = fd.read() # Read and process the file content...

    :param directory: the base directory.
    :param filename: the untrusted filename relative to that directory.
    :raises: :class:`~werkzeug.exceptions.NotFound` if the resulting path
    would fall out of `directory`.
    """
    filename = posixpath.normpath(filename)
    for sep in _os_alt_seps:
        if sep in filename:
            raise NotFound()
    if os.path.isabs(filename) or filename.startswith('../'):
        raise NotFound()
    return os.path.join(directory, filename)





class CMK_AWS_EC2_Info:
    def __init__(self, timestamp=0, tag_name="", pbd_abs="", pbf_rel=""):
        self.timestamp = timestamp
        self.tag_name = tag_name
        self.pbd_abs = pbd_abs
        self.pbf_rel = pbf_rel





cmk_sect_re = re.compile(r'<<<(.*?)[:.*|>>>]')
def extract_cmk_sections(filename, cmk_sections_filter=['']):
    ret = {}
    with open(filename, "r") as f:
        for line in f:
            if line.startswith('<<<'):
                curr_sect_re = cmk_sect_re.match(line)
                curr_sect = curr_sect_re.groups(1)[0]
                if ret:                                  ## if we already found previous sections, this delimiter ends the previous current section
                    ret[prev_sect] = curr_sect_contents  ## so push it in the results
                else:                                    ## this is the very 1st section (ret is still empty)
                    ret[curr_sect] = ''                  ## so we initialize it with an empty section

                curr_sect_contents = ''                  ## Reset the current section, so it is ready to accept new lines
                prev_sect = curr_sect

            else:
                if ret:                                  ## if we already found previous sections, this line can be added to the current section
                    curr_sect_contents += line

    if ret:
        ret[curr_sect] = curr_sect_contents              ## Append the last found lines to the current section

    ## of all sections, return only those starting with specified filter - TODO: this can be improved using a PREDICATE (lambda filter)
    return {k: v for k, v in ret.items() if any(k.startswith(s) for s in cmk_sections_filter)}




########################################################################################################
## MAIN
########################################################################################################

os.system('clear')


# get Check_MK root directory
HOMEDIR = os.getenv('HOME','~')
HOMEDIR = os.getenv('OMD_ROOT',HOMEDIR)

# Get CheckMK tmp fs , where piggyback data is stored
TMPDIR = os.path.join(HOMEDIR,'tmp')

## get current valid piggyback sources hosts
PIGGYBACK_SOURCES_DIR = os.path.join(HOMEDIR, 'tmp/check_mk/piggyback_sources/')
PIGGYBACK_SOURCES = os.listdir(PIGGYBACK_SOURCES_DIR)

# piggyback root directory, containing 1 dir for every piggy-backed host
PIGGYBACK_ROOTDIR = os.path.join(HOMEDIR, 'tmp/check_mk/piggyback/')


# Here we process only the AWS Agent hosts, like "ip-10-200-15-99.eu-west-1-i-0123456789abcdef0"
re_aws_dir = re.compile(r'(?:^|\b(?<!\.))(?:1?\d?\d|2[0-4]\d|25[0-5])(?:\.(?:1?\d?\d|2[0-4]\d|25[0-5])){3}(?=$|[^\w.])-.*-.*-.*-(i-[0-9a-f]+)$')
#                                                                                                                > regexp group:(instance_id)


# global association dict InstanceId -> CMK_AWS_EC2_Info
cmk_pb_info = {}


# search every piggyback directory (pbd) and look only for those named correctly, whose piggyback files (pbf) come from correct sources, etc
for pbd_rel in os.listdir(PIGGYBACK_ROOTDIR):
    pbd_abs = os.path.join(PIGGYBACK_ROOTDIR,pbd_rel)
    if os.path.isdir(pbd_abs) and not os.path.islink(pbd_abs):
        re_aws_dir_find = re_aws_dir.match(pbd_rel)
        if re_aws_dir_find and re_aws_dir_find.lastindex == 1: # inside each PBD:
            pbd_instanceid = re_aws_dir_find.group(1)  ## get ec2 instance id from PBD directory name

            for pbf_rel in os.listdir(pbd_abs):
                pbf_abs = os.path.join(pbd_abs,pbf_rel)
                if os.path.isfile(pbf_abs) and not os.path.islink(pbf_abs) and pbf_rel in PIGGYBACK_SOURCES:
                    cmk_sections = extract_cmk_sections(pbf_abs, ['aws_ec2','ec2_labels'])

                    if 'aws_ec2' in cmk_sections:

                        # This is only for CheckMK ver < 1.6 (where the EC2 Tags are already stored as section "ec2_labels")
                        if 'ec2_labels' not in cmk_sections:  ## LEGACY code will be called only if not present in cmk sections
                            cmk_sections['ec2_labels'] = generate_fake_ec2_labels(pbd_instanceid,legacy_ec2_tags_online.ec2tags[legacy_ec2_tags_online.regions[0]])

                        pbf_timestamp = os.path.getmtime(pbf_abs)

                        add_or_replace = False
                        if pbd_instanceid in cmk_pb_info: ## if instance is already present
                            if pbf_timestamp > cmk_pb_info[pbd_instanceid].timestamp:  ## if this file is newer, replace
                                add_or_replace = True
                        else:
                            add_or_replace = True


                        if add_or_replace:
                            try:
                                tagname = json.loads(cmk_sections['ec2_labels'])['Name']
                                cmk_pb_info[pbd_instanceid] = CMK_AWS_EC2_Info(timestamp=pbf_timestamp, tag_name=tagname, pbd_abs=pbd_abs, pbf_rel=pbf_rel )
                            except:
                                pass



# Symlinks for name tags
for i in cmk_pb_info:
    try:
        iv = cmk_pb_info[i]
        ln_target = os.path.basename(os.path.normpath(iv.pbd_abs))
        ln_name = safe_join(PIGGYBACK_ROOTDIR, iv.tag_name)
        if os.path.exists(ln_name):
            if os.path.islink(ln_name):
                if (os.path.realpath(ln_name) != os.path.realpath(safe_join(PIGGYBACK_ROOTDIR, ln_target))):
                    print("%s R> %s" % (ln_name,ln_target))
                    tmplnk = tempfile.mktemp(dir=TMPDIR)
                    os.symlink(ln_target, tmplnk)
                    os.rename(tmplnk, ln_name)
        else:
            print("%s -> %s" % (ln_name,ln_target))
            tmplnk = tempfile.mktemp(dir=TMPDIR)
            os.symlink(ln_target, tmplnk)
            os.rename(tmplnk, ln_name)

    except:
        pass ## simply skip abnormal name tags that would result in strange symlinks

