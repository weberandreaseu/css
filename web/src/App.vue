<template>
  <div id="app">
    <div id="nav">
      <div class="container">
        <router-link to="/">Home</router-link>
        <router-link to="/tracker">Tracker</router-link>
        <router-link to="/demo">Demo</router-link>
      </div>
    </div>
    <div class="container">
      <router-view />
    </div>
    <footer>
      <div class="container">
        Source code at
        <a href="https://github.com/weberandreaseu/css">GitHub</a>
      </div>
    </footer>
  </div>
</template>

<style>
body {
  margin: 0;
  /* padding: 15px; */
}
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}
#nav {
  padding: 25px 0;
  background-color: #ebebeb;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
  margin: 0 10px;
  text-decoration: none;
}

#nav a.router-link-exact-active {
  color: #42b983;
}

footer {
  padding: 25px 15px;
  background-color: #353535;
  color: #ebebeb;
}

footer a {
  color: #ebebeb;
}
.container {
  margin: 0 auto;
  max-width: 1024px;
  padding: 0 15px;
}
</style>
