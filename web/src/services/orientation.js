export default class Orientation {
  constructor () {
    this.alpha = 0
    this.beta = 0
    this.gamma = 0
    this.counter = 0
  }

  /**
   *
   * @param {Object} event  deviceMotionEvent containing alpha, beta, gamma
   */
  push (event) {
    this.alpha += event.alpha
    this.beta += event.beta
    this.gamma += event.gamma
    this.counter++
  }

  mean () {
    if (this.counter > 0) {
      return {
        alpha: this.alpha / this.counter,
        beta: this.beta / this.counter,
        gamma: this.gamma / this.counter
      }
    } else {
      return {
        alpha: 0,
        beta: 0,
        gamma: 0
      }
    }
  }

  reset () {
    this.alpha = 0
    this.beta = 0
    this.gamma = 0
    this.counter = 0
  }
}
