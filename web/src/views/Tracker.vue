<template>
  <div class="tracker">
    <h1>CSS Motion Tracker</h1>
    <p>
      This app collects sensor data of your smartphone and sends them to an influx database.
      The labeled movement data will be used to train an activity classifier.
    </p>

    <Warning msg="Device does not support sensor access" />

    <h3>Enter your data</h3>

    <p>
      Subject:
      <input type="text" name="name" id="subject" :value="uuid()" />
    </p>

    <span>Select an activity:</span>
    <select name="Activity" id="label">
      <option value="testing">Testing</option>
      <option value="biking">Biking</option>
      <option value="sitting">Sitting</option>
      <option value="walking">Walking</option>
    </select>

    <h3>Start Recording</h3>

    <ToogleButton/>

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
import Warning from '@/components/Warning.vue'
import ToogleButton from '@/components/ToogleButton.vue'
import { InfluxDB } from 'influx'
console.log('Influx: ' + InfluxDB)

export default {
  components: {
    Warning,
    ToogleButton
  },
  methods: {
    uuid: guidGenerator
  }
}

function guidGenerator () {
  var S4 = function () {
    return (((1 + Math.random()) * 0x10000) | 0).toString(16).substring(1)
  }
  return (S4() + S4() + '-' + S4() + '-' + S4() + '-' + S4() + '-' + S4() + S4() + S4())
}
</script>
