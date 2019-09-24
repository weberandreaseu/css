<template>
    <div class="warning">
        <b>{{ msg }}</b>
    </div>
</template>

<script>
export default {
  name: 'Warning',
  props: {
    msg: String
  }
}
</script>

<style>
.warning {
    background-color: #ffe3e3;;
    border-left: 10px solid #d9534f;
    color: #d9534f;
    padding: 20px;
}

</style>
