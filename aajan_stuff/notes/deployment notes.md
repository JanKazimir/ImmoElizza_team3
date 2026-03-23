# Deployment notes

Morning on study. Let's set up the repo squeecky clean.

Read the readme

## Instructions:
Deploy an api that can query the model.
    The api works with JSON
    for each route : what is the input, what is the output
    provide error if something goes wrong

we need an app.py for the api
folders:
- deploy 
    - preprocessing, (has cleaning_data.py with preprocess())
    - model : at the root 
    - predict (the code to predict a price)

### Preprocessing pipeline:
This is where we preprocess the data coming in from the user that wants to predict a price. 
What format we'll need for the model? 
what needs to be there, what can be nan.
- cleaning_data.py
  - has a preprocess() function, takes the input returns the preprocessed data, or an error to the user.

### Prediction:
- model/ folder at the root contains the model
- predict/ 
  - prediction.py with predict() takes the preprocessed data and returns the price as output


### Api
In your `app.py` file, create an API that contains:

- A route at `/` that accept:
  - `GET` request and return `"alive"` if the server is alive.
- A route at `/predict` that accept:
  - `POST` request that receives the data of a house in JSON format.
  - `GET` request returning a string to explain what the `POST` expect (data and format).

### 5 Docker image
### 6 deploy docker to render.com


### Document the API
- a readme
- what routes are available with what methods
- data format
- output in case of success / error

### Present
- presentation for the webdevs (no code)
- present the documentation




####  The JSON format must be: 
But we don't have to use all fields
(address will be annoying)

```json
{
  "data": {
    "area": int,
    "property-type": "APARTMENT" | "HOUSE" | "OTHERS",
    "rooms-number": int,
    "zip-code": int,
    "land-area": Optional[int],
    "garden": Optional[bool],
    "garden-area": Optional[int],
    "equipped-kitchen": Optional[bool],
    "full-address": Optional[str],
    "swimming-pool": Optional[bool],
    "furnished": Optional[bool],
    "open-fire": Optional[bool],
    "terrace": Optional[bool],
    "terrace-area": Optional[int],
    "facades-number": Optional[int],
    "building-state": Optional[
      "NEW" | "GOOD" | "TO RENOVATE" | "JUST RENOVATED" | "TO REBUILD"
    ]
  }
}
```

```json
{
  "prediction": Optional[float],
  "status_code": Optional[int]
}
```


## Deliverables

1. Pimp up the README file:
   - Description
   - Installation
   - Usage
   - (Visuals)
   - (Contributors)
   - (Timeline)
   - (Personal situation)
2. Use Docker to wrap your API.
3. Your API is deployed on Render.
4. You documentation is clear.

## Evaluation criteria

| Criteria       | Indicator                                                | Yes/No |
| -------------- | -------------------------------------------------------- | ------ |
| 1. Is complete | Your API works.                                          | [ ]    |
|                | The API is clear and the presentation is understandable. | [ ]    |
|                | README is pimped.                                        | [ ]    |
|                | Your model is trained and can predict a result.          | [ ]    |
|                | Your API is deployed on Render with Docker.              | [ ]    |
| 2. Is good     | The repo doesn't contain unnecessary files.              | [ ]    |
|                | You used typing.                                         | [ ]    |
|                | The presentation is clean.                               | [ ]    |
|                | The web-dev group understood well how your API works.    | [ ]    |
