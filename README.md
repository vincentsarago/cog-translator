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
