cog_translator
==============

[`ecs-watchbot-fargate`](https://github.com/vincentsarago/ecs-watchbot-fargate) example to create a simple/self-managed processing pipeline using ECS Fargate.

`ecs-watchbot-fargate` is based on `@mapbox/ecs-watchbot`, please refer to https://github.com/mapbox/ecs-watchbot for more information

Install and Deploy
------------------

**prerequisites**

- `cloudformation-kms-production` deployed according to the instructions in [cloudformation-kms](https://github.com/mapbox/cloudformation-kms). Makes encryption of sensitive environment variables that need to be passed to ECS simple using [cfn-config](https://github.com/mapbox/cfn-config).

- Install `@mapbox/cfn-config` and follow https://github.com/mapbox/cfn-config#prerequisites

  ```bash
  $ npm install -g @mapbox/cfn-config
  ```

**Deploy**
- Create a Fargate Cluster [link](link)

- add docker image in your ecr repository
  - edit [Makefile](https://github.com/vincentsarago/cog-translator/blob/master/Makefile) (update service region, name, or version)
  - `make push`

- Install dependencies

  ```bash
  $ npm install
  ```

- deploy

  ```bash
  $ cfn-config create production cloudformation/cog-translator.template.js -c mybucket-configs

  ? AlarmEmail. Email address: contact@remotepixel.ca
  ? Bucket. Bucket to grant stack PUT access to: remotepixel-pub
  ? Cluster. Cluster name or ARN: fargate-cluster
  ? CpuAllocation. CPU allocation: 2048
  ? ErrorThreshold. Error threshold for alert: 10
  ? ImageVersion: 1.0.0
  ? MemoryAllocation. Memory allocation (Mb): 12288
  ? minSize. Minimum workers size.: 0
  ? maxSize. Maximum worker size: 10
  ```


Use
---

Once your stack is up and running we can send message to the AWS SQS queue. By design ecs-watchbot will scale your fargate task up and down depending on how many messages are left in the queue (AWS lambda will run every 5min to check the SQS queue).

We first need to get the SNS topic for our cog-translate-production stack

```bash
$ aws cloudformation describe-stacks --stack-name cog-translator-production | jq -r '.Stacks[0].Outputs[] | select(.OutputKey == "SnsTopic") | .OutputValue'

arn:aws:sns:{REGION}:{MY-AWS-ACCOUNT-ID}:cog-translator-production-WatchbotTopic-{STACK-VERSION}
```


```bash
$ python scripts/feed.py https://my-url.tif \
  --bucket my-bucket \
  --key dir/dir/my-cog.tif
  --topic arn:aws:sns:{REGION}:{MY-AWS-ACCOUNT-ID}:cog-translator-production-WatchbotTopic-{STACK-VERSION}
```


Example
-------

In this example we'll  convert huge GeoTIFF from DG opendata repository to COG.

###### 1. Get file list

```python
import requests
import bs4 as BeautifulSoup

url = 'https://www.digitalglobe.com/opendata/super-typhoon-yutu/post-event'

# Read Page
r = requests.get(url)

# Use BeautifulSoup to parse and extract all imagey links
soup = BeautifulSoup.BeautifulSoup(r.text)
s = soup.findAll('a',attrs={"class":"opendata__tilelinks"})

list_file = list(set([l.get('href') for l in s if not l.get('href').endswith('ovr')]))

with open('list_dg_yutu.txt', 'w') as f:
    f.write('\n'.join(list_file))
```

```bash
$ cat list_dg_yutu.txt
http://opendata.digitalglobe.com/cyclone-yutu/post-event/2018-10-26/10400100458B5A00/1313220.tif
http://opendata.digitalglobe.com/cyclone-yutu/post-event/2018-10-26/10400100458B5A00/1313030.tif
http://opendata.digitalglobe.com/cyclone-yutu/post-event/2018-10-26/10400100458B5A00/1313230.tif
http://opendata.digitalglobe.com/cyclone-yutu/post-event/2018-10-26/10400100458B5A00/1313001.tif
http://opendata.digitalglobe.com/cyclone-yutu/post-event/2018-10-26/10400100458B5A00/1313203.tif
http://opendata.digitalglobe.com/cyclone-yutu/post-event/2018-10-26/10400100458B5A00/1313012.tif
http://opendata.digitalglobe.com/cyclone-yutu/post-event/2018-10-26/10400100458B5A00/1313213.tif
http://opendata.digitalglobe.com/cyclone-yutu/post-event/2018-10-26/10400100458B5A00/1313221.tif
http://opendata.digitalglobe.com/cyclone-yutu/post-event/2018-10-26/10400100458B5A00/1313020.tif
http://opendata.digitalglobe.com/cyclone-yutu/post-event/2018-10-26/10400100458B5A00/1313000.tif
http://opendata.digitalglobe.com/cyclone-yutu/post-event/2018-10-26/10400100458B5A00/1313031.tif
http://opendata.digitalglobe.com/cyclone-yutu/post-event/2018-10-26/10400100458B5A00/1313022.tif
http://opendata.digitalglobe.com/cyclone-yutu/post-event/2018-10-26/10400100458B5A00/1313212.tif
http://opendata.digitalglobe.com/cyclone-yutu/post-event/2018-10-26/10400100458B5A00/1313010.tif
http://opendata.digitalglobe.com/cyclone-yutu/post-event/2018-10-26/10400100458B5A00/1313013.tif
http://opendata.digitalglobe.com/cyclone-yutu/post-event/2018-10-26/10400100458B5A00/1313011.tif
http://opendata.digitalglobe.com/cyclone-yutu/post-event/2018-10-26/10400100458B5A00/1313021.tif
http://opendata.digitalglobe.com/cyclone-yutu/post-event/2018-10-26/10400100458B5A00/1313202.tif
http://opendata.digitalglobe.com/cyclone-yutu/post-event/2018-10-26/10400100458B5A00/1313200.tif
http://opendata.digitalglobe.com/cyclone-yutu/post-event/2018-10-26/10400100458B5A00/1313023.tif
http://opendata.digitalglobe.com/cyclone-yutu/post-event/2018-10-26/10400100458B5A00/1313231.tif
http://opendata.digitalglobe.com/cyclone-yutu/post-event/2018-10-26/10400100458B5A00/1313033.tif
http://opendata.digitalglobe.com/cyclone-yutu/post-event/2018-10-26/10400100458B5A00/1313201.tif
http://opendata.digitalglobe.com/cyclone-yutu/post-event/2018-10-26/10400100458B5A00/1313210.tif
http://opendata.digitalglobe.com/cyclone-yutu/post-event/2018-10-26/10400100458B5A00/1313002.tif
http://opendata.digitalglobe.com/cyclone-yutu/post-event/2018-10-26/10400100458B5A00/1313003.tif
http://opendata.digitalglobe.com/cyclone-yutu/post-event/2018-10-26/10400100458B5A00/1313211.tif
http://opendata.digitalglobe.com/cyclone-yutu/post-event/2018-10-26/10400100458B5A00/1313032.tif
```

###### 2. Get stack topic
```bash
$ topic=$(aws cloudformation describe-stacks --stack-name cog-translator-production | jq -r '.Stacks[0].Outputs[] | select(.OutputKey == "SnsTopic") | .OutputValue')
```

###### 3. Send work to our stack

```bash
$ bucket=opendata.remotepixe.ca
$ prefix=dg_post_yutu/

$ cat list_dg_yutu.txt | while read line; do; date=$(echo $line | cut -d'/' -f6 | sed 's/-/_/g'); bname=$(echo $line | cut -d'/' -f8); python scripts/feed.py $line --bucket $bucket --key $prefix$date/$bname --topic $topic; done
```

###### 4. Get a :coffee:

###### 5. Data overview

Converting the tif to COG we created a set of data that weight 421Mb, far from the original ~29Gb hosted by DG.

```bash
$ aws s3 ls s3://opendata.remotepixel.ca/dg_post_yutu/20181026/ --human --summarize
2018-11-02 23:49:57    3.4 MiB 1313000.tif
2018-11-02 23:49:57    3.4 MiB 1313001.tif
2018-11-02 23:49:57    5.1 MiB 1313002.tif
2018-11-02 23:49:57   16.9 MiB 1313003.tif
2018-11-02 23:49:57    3.4 MiB 1313010.tif
2018-11-02 23:49:57    4.0 MiB 1313011.tif
2018-11-02 23:49:57   18.0 MiB 1313012.tif
2018-11-02 23:49:57   18.3 MiB 1313013.tif
2018-11-02 23:49:57    8.8 MiB 1313020.tif
2018-11-02 23:49:57   30.3 MiB 1313021.tif
2018-11-02 23:49:57    7.4 MiB 1313022.tif
2018-11-02 23:49:57   26.2 MiB 1313023.tif
2018-11-02 23:49:57   22.3 MiB 1313030.tif
2018-11-02 23:49:58   17.7 MiB 1313031.tif
2018-11-02 23:49:58   20.3 MiB 1313033.tif
2018-11-02 23:49:58    5.3 MiB 1313200.tif
2018-11-02 23:49:58   26.1 MiB 1313201.tif
2018-11-02 23:49:58    6.6 MiB 1313202.tif
2018-11-02 23:49:59   24.5 MiB 1313203.tif
2018-11-02 23:49:59   33.4 MiB 1313210.tif
2018-11-02 23:49:59   22.7 MiB 1313211.tif
2018-11-02 23:49:59   29.1 MiB 1313212.tif
2018-11-02 23:50:00   21.7 MiB 1313213.tif
2018-11-02 23:50:00    6.2 MiB 1313220.tif
2018-11-02 23:50:00   18.6 MiB 1313221.tif
2018-11-02 23:50:00   10.7 MiB 1313230.tif
2018-11-02 23:50:00   10.8 MiB 1313231.tif

Total Objects: 27
   Total Size: 421.3 MiB
```

###### 5. Use the data
```bash
$ pip install rio-glui

$ rio glui https://s3.amazonaws.com/opendata.remotepixel.ca/dg_post_yutu/20181026/1313021.tif
```

![](https://user-images.githubusercontent.com/10407788/47956729-a234a580-df7f-11e8-9e22-f332bb348459.jpg)
