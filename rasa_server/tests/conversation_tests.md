#### This file contains tests to evaluate that your bot behaves as expected.
#### If you want to learn more, please see the docs: https://rasa.com/docs/rasa/user-guide/testing-your-assistant/

## happy path 1
* greet: 你好
  - utter_greet
* mood_great: 很好
  - utter_happy

## happy path 2
* greet: 你好
  - utter_greet
* mood_great: 很好
  - utter_happy
* goodbye: 再见
  - utter_goodbye

## sad path 1
* greet: 你好
  - utter_greet
* mood_unhappy: 很难过
  - utter_cheer_up
  - utter_did_that_help
* affirm: 是的
  - utter_happy

## sad path 2
* greet: 你好
  - utter_greet
* mood_unhappy: 很难过
  - utter_cheer_up
  - utter_did_that_help
* deny: 没有
  - utter_goodbye

## sad path 3
* greet: 你好
  - utter_greet
* mood_unhappy: 很难过
  - utter_cheer_up
  - utter_did_that_help
* deny: 没有
  - utter_goodbye

## say goodbye
* goodbye: 再见
  - utter_goodbye

## ask weather 1
* ask_weather: 天气怎么样
  - utter_ask_city
* 
