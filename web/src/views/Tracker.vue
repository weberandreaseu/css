<template>
  <div class="tracker">
    <h1>Motion Tracker</h1>
    <p>
      This app collects sensor data of your smartphone and sends them to an influx database.
      The labeled movement data will be used to train an activity classifier.
    </p>

    <OrientationSupport/>
    <!-- <div class="banner" v-bind:class="[ sensorSupport ? 'success' : 'warning' ]">
      <span v-if="sensorSupport">Supports device orientation</span>
      <span v-else>Does not support device orientation</span>
    </div> -->

    <h3>Select your activity:</h3>
    <select v-model="activity" :disabled="isRecording">
      <option value="testing">Testing</option>
      <option value="sitting">Sitting</option>
      <option value="walking">Walking</option>
      <option value="calling">Calling</option>
    </select>

    <h3>Start Recording</h3>

    <button v-if="isRecording" v-on:click="stopRecording()">Stop recording</button>
    <button v-else v-on:click="startRecording()" :disabled="!sensorSupport">Start recording</button>

    <ul class="sensor-values">
      <li>Counter: {{ counter }}</li>
      <li>Alpha: {{ alpha }}</li>
      <li>Beta: {{ beta }}</li>
      <li>Gamma: {{ gamma }}</li>
    </ul>
  </div>
</template>

<script>
import { InfluxDB } from 'influx'
import Orientation from '../services/orientation'
import OrientationSupport from '@/components/OrientationSupport'

export default {
  components: { OrientationSupport },
  data: function () {
    return {
      isRecording: false,
      activity: 'testing',
      counter: 0,
      alpha: 0,
      beta: 0,
      gamma: 0
    }
  },
  methods: {
    uuid: function () {
      var S4 = function () {
        return (((1 + Math.random()) * 0x10000) | 0).toString(16).substring(1)
      }
      return (S4() + '-' + S4() + '-' + S4())
    },
    startRecording: function () {
      this.isRecording = true
      this.id = this.uuid()
      this.interval = setInterval(this.sendSamples, 1000 / 20)
      this.orientation = new Orientation()
      console.log('Start recording')
    },
    stopRecording: function () {
      this.isRecording = false
      this.counter = 0
      console.log('Stop recording')
      clearInterval(this.interval)
    },
    sendSamples: function () {
      if (this.orientation.counter <= 0) { return }
      this.counter++
      var values = this.orientation.mean()
      this.orientation.reset()
      this.client.writeMeasurement('orientation', [
        {
          key: 'orientation',
          tags: {
            label: this.activity,
            subject: this.id
          },
          fields: {
            count: this.counter,
            alpha: values[0],
            beta: values[1],
            gamma: values[2]
          },
          timestamp: (Date.now() * 1000000)
        }
      ])
    }
  },
  computed: {
    sensorSupport: function () {
      return window.DeviceOrientationEvent
    }
  },
  created: function () {
    // create influxdb client
    const client = new InfluxDB({
      database: 'css',
      host: 'influxdb.weberandreas.eu',
      protocol: 'https',
      port: 443,
      username: 'admin',
      password: 'css-secret-password'
    })
    this.client = client
    // ping database to test connection
    async function ping (client) {
      const ping = await client.ping()
      console.log('Ping influxdb status code: ' + ping[0].res.statusCode)
    }
    ping(this.client)
    // register callback to collect sensor data
    window.addEventListener('deviceorientation', (event) => {
      if (!this.isRecording) return
      this.alpha = event.alpha
      this.beta = event.beta
      this.gamma = event.gamma
      this.orientation.push(event)
    })
  }
  // destroyed: function () {
  //   window.removeEventListener('deviceorientation', deviceOrientationHandler, false)
  // }
}
</script>

<style>
ul.sensor-values {
  list-style-type: none;
  padding: 0;
}
ul.sensor-values li {
  padding: 4px 0;
}
</style>
