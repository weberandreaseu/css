<template>
  <div class="home">
    <!-- <img alt="Vue logo" src="../assets/logo.png"> -->
    <!-- <HelloWorld msg="Welcome to Your Vue.js App"/> -->
    <h1>Context Sensitive System</h1>
    <p>
      This application is part of the lecture <i>context sensitive systems</i>.
      A context sensitive system captures relevant data to improve the users interaction with the system for a given application.
      Based on the data, the system fits a model that predicts the users current context.
      With the predicted context, the system can adapt to the users needs and make the interaction with the application more efficient.
    </p>
    <p>
      Here, the <a href="/tracker">tracker app</a>
      collects sensor data together with a label for current activity and stores them in an Influx database.
      Based on those measurements, a random forest classifier is trained to predict the current activity.
      The <a href="/radio">radio app</a> applies live sensor data to this model and adapts played songs to the predicted activity. 
    </p>
  </div>
</template>
