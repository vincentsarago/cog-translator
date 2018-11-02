
const cf = require('@mapbox/cloudfriend')
const watchbot = require('watchbot-fargate')

const params = {
  Parameters: {
    AlarmEmail: {
      Description: 'Email address',
      Type: 'String'
    },
    Bucket: {
      Description: 'Bucket to grant PUT access to',
      Type: 'String'
    },
    Cluster: {
      Type: 'String',
      Description: 'Cluster name or ARN'
    },
    ClusterSubnets: {
      Type: 'CommaDelimitedList',
      Description: 'Cluster\'s subnets'
    },
    CpuAllocation: {
      Description: 'CPU allocation',
      Type: 'Number',
      Default: 256
    },
    ErrorThreshold: {
      Type: 'Number',
      Description: 'Error threshold for alert',
      Default: 10,
      MinValue: 0
    },
    ImageVersion: {
      Type: 'String'
    },
    MemoryAllocation: {
      Description: 'Memory allocation (Mb)',
      Type: 'Number',
      Default: 2048
    },
    minSize: {
      Type: 'Number',
      Description: 'Minimum workers size.',
      Default: 0,
      MinValue: 0,
      MaxValue: 10
    },
    maxSize: {
      Type: 'Number',
      Description: 'Maximum worker size',
      Default: 10,
      MinValue: 1,
      MaxValue: 100
    }
  }
}

const stack = watchbot.template({
  service: 'cog-translator',
  serviceVersion: cf.ref('ImageVersion'),
  command: 'python3 -m cog_translator.scripts.cli',
  cluster: cf.ref('Cluster'),
  cpu: cf.ref('CpuAllocation'),
  memory: cf.ref('MemoryAllocation'),
  minSize: cf.ref('minSize'),
  maxSize: cf.ref('maxSize'),
  notificationEmail: cf.ref('AlarmEmail'),
  errorThreshold: cf.ref('ErrorThreshold'),
  maxJobDuration: 12600,
  permissions: [
    {
      Action: [
        's3:PutObject',
        's3:PutObjectAcl'
      ],
      Effect: 'Allow',
      Resource: [
        cf.join(['arn:aws:s3:::', cf.ref('Bucket'), '*'])
      ]
    }
  ],
  publicIp: 'ENABLED',
  subnets: cf.ref('ClusterSubnets')
})
// We add SNSTopic in the outputs (ref: https://github.com/mapbox/ecs-watchbot/issues/271)
stack.Outputs.SnsTopic = { Value: stack.ref.topic }

module.exports = cf.merge(params, stack)
