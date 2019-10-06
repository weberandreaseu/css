const rockSong = new Audio('https://www.bensound.org/bensound-music/bensound-happyrock.mp3')
const jazzSong = new Audio('https://www.bensound.org/bensound-music/bensound-thejazzpiano.mp3')

export default function getSong (activity) {
  if (activity.toLowerCase() === 'walking') {
    return rockSong
  } else {
    return jazzSong
  }
}
