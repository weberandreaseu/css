<template>
  <div class="tracker">
    <h1>CSS Motion Tracker</h1>
    <p>
      This app collects sensor data of your smartphone and sends them to an influx database.
      The labeled movement data will be used to train an activity classifier.
    </p>

    <div class="banner" v-bind:class="[ sensorSupport ? 'success' : 'warning' ]">
      <span v-if="sensorSupport">Supports device orientation</span>
      <span v-else>Does not support device orientation</span>
    </div>

    <h3>Enter your data</h3>

    <span>Select an activity:</span>
    <select name="Activity" id="label" :disabled="isRecording">
      <option value="testing">Testing</option>
      <option value="sitting">Sitting</option>
      <option value="walking">Walking</option>
      <option value="calling">Calling</option>
    </select>

    <h3>Start Recording</h3>

    <button v-if="isRecording" v-on:click="stopRecording()">Stop recording</button>
    <button v-else v-on:click="startRecording()" :disabled="!sensorSupport">Start recording</button>

    <!-- <label class="switch">
        <input id="recordingButton" type="checkbox" disabled="true" />
        <span class="slider round"></span>
    </label> -->
    <!-- <ToogleButton/> -->

    <p>Counter: {{ counter }}</p>
    <div class="sensor-values">
      <p>
        Alpha:
        <span id="alpha">{{ alpha }}</span>
      </p>
      <p>
        Beta:
        <span id="beta">{{ beta }}</span>
      </p>
      <p>
        Gamma:
        <span id="gamma">{{ gamma }}</span>
      </p>
    </div>
  </div>
</template>

<script>
import { InfluxDB } from 'influx'
import Orientation from '../services/orientation'

export default {
  data: function () {
    return {
      isRecording: false,
      counter: 0,
      alpha: 0,
      beta: 0,
      gamma: 0
    }
  },
  // TODO refactor recording in own component with create and destroy hook
  // https://css-tricks.com/creating-vue-js-component-instances-programmatically/
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
      var label = document.getElementById('label').value
      this.client.writeMeasurement('orientation', [
        {
          key: 'orientation',
          tags: {
            label: label,
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
.banner {
  padding: 20px;
}

.warning {
    background-color: #ffe3e3;;
    border-left: 10px solid #d9534f;
    color: #d9534f;
}

.success {
    background-color: #c8ffdb;;
    border-left: 10px solid #00b528;
    color: #00b528;
}
</style>
