<template>
    <div class="banner" v-bind:class="[ sensorSupport ? 'success' : 'warning' ]">
      <span v-if="sensorSupport">Device supports orientation sensors</span>
      <span v-else>Device does not support orientation sensors</span>
    </div>
</template>

<script>
export default {
  name: 'OrientationSupport',
  computed: {
    sensorSupport: function () {
      return window.DeviceOrientationEvent
    }
  }
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
    background-color: #c7ffe6;
    border-left: 10px solid #42b983;
    color: #42b983;
}
</style>
