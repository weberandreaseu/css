# Context Sensitive Systems

This application is part of the lecture _context sensitive systems_.
A context sensitive system captures relevant data to improve the users interaction with the system for a given application.
Based on the data, the system fits a model that predicts the users current context.
With the predicted context, the system can adapt to the users needs and make the interaction with the application more efficient.

The application has two components:
The [tracker](https://css.weberandreas.eu/tracker)
collects sensor data together with a label for current activity and stores them in an Influx database.
Based on those measurements, a random forest classifier is trained to predict the current activity.
The [radio app](https://css.weberandreas.eu/radio) applies live sensor data to this model and adapts played songs to the predicted activity. 

## Roadmap
- [x] Use VS Code remote containers
- [x] Learn and setup Webpack/Vue
- [x] Setup InfluxDB
- [x] Integrate influx db client in browser
- [x] Build a web app storing smartphone sensor data into InfluxDB
- [x] Train a model to predict activities
- [x] Deploy model into another web app