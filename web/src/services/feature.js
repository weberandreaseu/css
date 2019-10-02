function sum (total, num) {
  return total + num
}

function mean (arr) {
  if (arr.length === 0) return 0
  return arr.reduce(sum) / arr.length
}

function variance (arr) {
  const m = mean(arr)
  // calc difference to mean
  const variance = arr.map(x => x - m)
    // square the difference
    .map(x => x * x)
    // sum of squared values
    .reduce(sum)
  // nomalize
  return variance / (arr.length - 1)
}

export default class Feature {
  constructor () {
    this.alpha = []
    this.beta = []
    this.gamma = []
    this.counter = []
  }

  push (measurement) {
    this.alpha.push(measurement.alpha)
    this.beta.push(measurement.beta)
    this.gamma.push(measurement.gamma)
    this.counter++
  }

  reset () {
    this.alpha = []
    this.beta = []
    this.gamma = []
    this.counter = []
  }

  getFeatures () {
    const features = [
      mean(this.alpha),
      mean(this.beta),
      mean(this.gamma),
      variance(this.alpha),
      variance(this.beta),
      variance(this.gamma)
    ]
    this.reset()
    return features
  }
}
