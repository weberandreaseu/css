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

    <p>Current context: {{ mood }}</p>

    <button v-on:click="playSong()">Play song</button>
    <button v-on:click="stopSong()">Stop song</button>

  </div>
</template>

<script>

var song = new Audio('https://www.bensound.org/bensound-music/bensound-thejazzpiano.mp3')
song.play()
export default {
  methods: {
    playSong: function () {
      song.play()
    },
    stopSong: function () {
      song.pause()
      song.currentTime = 0
    }
  }
}

if (typeof process !== 'undefined' && typeof process.argv !== 'undefined') {
    if (process.argv.length - 2 === 3) {

        // Features:
        var features = process.argv.slice(2);

        // Prediction:
        var clf = new DecisionTreeClassifier();
        var prediction = clf.predict(features);
        console.log(prediction);

    }
}

// var song = new Audio('https://www.bensound.org/bensound-music/bensound-happyrock.mp3')
song.play()

</script>
