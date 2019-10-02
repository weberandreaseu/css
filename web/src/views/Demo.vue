<template>
  <div class="demo">
    <h1>Song for mood</h1>

    <p>This app adapts the music style to your current context</p>

    <ul>
      <li>Active when walking</li>
      <li>Chill when sitting</li>
      <li>Mute when calling</li>
    </ul>

    <p>Take this, Spotify! 😉</p>

    <p>Move your smartphone to influce the music.</p>

    <p>Current activity: {{ activity }}</p>

    <button v-on:click="playSong()">Play song</button>
    <button v-on:click="stopSong()">Stop song</button>

    <ul class="sensor-values">
      <li>Alpha: {{ alpha }}</li>
      <li>Beta: {{ beta }}</li>
      <li>Gamma: {{ gamma }}</li>
    </ul>
  </div>
</template>

<script>
import Orientation from '../services/orientation'
import Feature from '../services/feature'

// import {DecisionTreeClassifier} from '../../static/model.js'

// var song = new Audio('https://www.bensound.org/bensound-music/bensound-thejazzpiano.mp3')
// song.play()
export default {
  data: function () {
    return {
      activity: 'testing',
      alpha: 0,
      beta: 0,
      gamma: 0
    }
  },
  methods: {
    // playSong: function () {
    //   song.play()
    // },
    // stopSong: function () {
    //   song.pause()
    //   song.currentTime = 0
    // },
    predictActivity: function () {
      const features = this.feature.getFeatures()
      if (features.length > 0)
        this.activity = this.classifier.predict(features)
    },
    pushSensorData: function () {
      if (this.orientation.counter > 0) {
        const features = this.orientation.mean()
        this.orientation.reset()
        this.feature.push(features)
      }
    }
  },
  computed: {
    sensorSupport: function () {
      return window.DeviceOrientationEvent
    }
  },
  created: function () {
    this.orientation = new Orientation()
    this.classifier = new DecisionTreeClassifier()
    this.feature = new Feature()
    // push sensor data 20 times per second
    setInterval(this.pushSensorData, 1000 / 20)
    // predect actifity each second
    setInterval(this.predictActivity, 1000)
    window.addEventListener('deviceorientation', (event) => {
      this.alpha = event.alpha
      this.beta = event.beta
      this.gamma = event.gamma
      this.orientation.push(event)
    })
  }
}
// var song = new Audio('https://www.bensound.org/bensound-music/bensound-happyrock.mp3')
</script>
