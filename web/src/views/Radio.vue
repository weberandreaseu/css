<template>
  <div class="radio">
    <h1>Adaptive Radio</h1>

    <p>The only radio station which adapts to your current activity:</p>

    <ul>
      <li>Play rock when walking</li>
      <li>Play jazz when sitting</li>
      <li>Mute when calling</li>
    </ul>

    <p>Take this, Spotify! 😉</p>

    <p>Move your smartphone to influce the music.</p>

    <OrientationSupport/>

    <p>Current activity: {{ activity }}</p>

    <button v-on:click="playSong()">Play song</button>
    <button v-on:click="pauseSong()">Pause song</button>
  </div>
</template>

<script>
import Orientation from '../services/orientation'
import OrientationSupport from '@/components/OrientationSupport'
import Feature from '../services/feature'
import getSong from '../services/songs'

const labels = new Map([
  [0, 'calling'],
  [1, 'sitting'],
  [2, 'walking']
])

export default {
  components: { OrientationSupport },
  data: function () {
    return {
      activity: 'calling',
      muted: false
    }
  },
  methods: {
    playSong: function () {
      this.muted = false
      if (this.song && this.song.paused) {
        this.song.play()
      }
    },
    pauseSong: function () {
      this.muted = true
      if (this.song && !this.song.paused) {
        this.song.pause()
      }
    },
    predictActivity: function () {
      const features = this.feature.getFeatures()
      if (features.length > 0) {
        const yPred = this.classifier.predict(features)
        const predActivity = labels.get(yPred)
        const prevActivity = this.activity
        this.activity = predActivity
        // if muted no change required
        if (this.muted) {
          return
        }
        // if calling, pause song
        if (predActivity === 'calling') {
          if (this.song && !this.song.paused) {
            this.song.pause()
          }
        // only change song if activity change
        } else if (prevActivity !== predActivity) {
          if (this.song && !this.song.paused) {
            this.song.pause()
          }
          this.song = getSong(predActivity)
          // resume the song or play
          this.song.play()
        }
      }
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
    this.classifier = new RandomForestClassifier()
    this.feature = new Feature()
    // push sensor data 20 times per second
    setInterval(this.pushSensorData, 1000 / 20)
    // predect activity each second
    setInterval(this.predictActivity, 1000)
    window.addEventListener('deviceorientation', (event) => {
      this.orientation.push(event)
    })
  }
}
</script>
