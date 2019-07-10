# Helper Script to create AWS EC2 piggyback data named after Name-Tags and not FQDN/InstanceIDs

v1.0 - initial release:
Author: Davide Del Grande <davide.delgrande _ lanewan.it> / <delgrande.davide _ gmail.com>

This is supposed to run as a OMD site cron job (`~/etc/cron.d/aws_piggyback_nametag_symlinks`) every minute, eg:
```
 * * * * * $OMD_ROOT/local/lib/aws_piggyback_nametag_symlinks.py >/dev/null 2>&1
```
In CheckMK 1.6, section "`ec2_labels`" already contains the aws tags associated with the instances, so they are extracted without api calls.
In CheckMK 1.5, this section is not present, so we extract it via AWS api call.
 - this *requires* that an EC2 instance role with appropriate permissions is associated to the monitoring machine
 - if this is not possible, you may try to use boto3 configuration files (aws configure) - but I have not tested it
 - permissions should be `EC2::DescribeTags` or alike
 - please change the script to use your AWS region/s - look for aws_regions = `"eu-west-1".split()`


The script will:
- enumerate all AWS piggyback directories under `~/tmp/check_mk/piggyback/` (named like "IP-region-instanceId")
- enumerate all files inside and build an association instance-id -> name-tag (if present)
- create a symlink "name-tag" -> piggyback directory (trying to filter out potentially dangerous namings)
- overwrite existing symlinks if instance-id has changed (eg EC2 instance recycling)


If you name CMK hosts for EC2 with their Name Tags, at next discovery, it should find the aws data.
This is working
