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

    <p>
      Subject:
      <input type="text" name="name" id="subject" :value="uuid()" />
    </p>

    <span>Select an activity:</span>
    <select name="Activity" id="label" :disabled="isRecording">
      <option value="testing">Testing</option>
      <option value="biking">Biking</option>
      <option value="sitting">Sitting</option>
      <option value="walking">Walking</option>
    </select>

    <h3>Start Recording</h3>

    <button v-if="isRecording" v-on:click="stopRecording()">Stop recording</button>
    <button v-else v-on:click="startRecording()" :disabled="!sensorSupport">Start recording</button>

    <!-- <label class="switch">
        <input id="recordingButton" type="checkbox" disabled="true" />
        <span class="slider round"></span>
    </label> -->
    <!-- <ToogleButton/> -->

    <div class="sensor-values">
      <p>
        Alpha:
        <span id="alpha"></span>
      </p>
      <p>
        Beta:
        <span id="beta"></span>
      </p>
      <p>
        Gamma:
        <span id="gamma"></span>
      </p>
    </div>
  </div>
</template>

<script>
// import Warning from '@/components/Warning.vue'
// import ToogleButton from '@/components/ToogleButton.vue'
import { InfluxDB } from 'influx'

export default {
  // components: {
  //   // Warning,
  //   // ToogleButton
  // },
  data: function () {
    return {
      isRecording: false
    }
  },
  methods: {
    uuid: guidGenerator,
    startRecording: function () {
      this.isRecording = true
      console.log('Start recording')
    },
    stopRecording: function () {
      this.isRecording = false
      console.log('Stop recording')
    }
  },
  computed: {
    sensorSupport: function () {
      return window.DeviceOrientationEvent
    }
  }
}

const client = new InfluxDB({
  database: 'css',
  host: 'localhost',
  port: 8086,
  username: '',
  password: ''
})

async function ping () {
  const ping = await client.ping()
  console.log(ping)
}
ping()

function guidGenerator () {
  var S4 = function () {
    return (((1 + Math.random()) * 0x10000) | 0).toString(16).substring(1)
  }
  return (S4() + S4() + '-' + S4() + '-' + S4() + '-' + S4() + '-' + S4() + S4() + S4())
}

// function startRecording () {
//   console.log('Start recording..')
// }

// function deviceOrientationHandler (event) {
//   document.getElementById('alpha').innerText = event.alpha
//   document.getElementById('beta').innerText = event.beta
//   document.getElementById('gamma').innerText = event.gamma
//   // samples.push(event.alpha, event.beta, event.gamma)
// }

// if (window.DeviceOrientationEvent) {
//   // document.getElementById('recordingButton').disabled = false
//   // var support = document.getElementById('support')
//   // console.log(support)
//   // // support.innerText = 'Your device supports orientation'
//   // // support.className = 'success'
//   // window.addEventListener('deviceorientation', deviceOrientationHandler, false)
// }

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
