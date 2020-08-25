import React, { Component } from 'react';

import './styles.css';

const server = "http://104.154.101.183:5000"
const headers = {
  'Accept': 'application/json'
}
const topics = ['love','dog','cat','life','friend','school','spring','summer','basketball',
  'rain', 'mom', 'blue', 'snow', 'brother', 'sky', 'winter', 'family', 'football',
  'sister', 'bird', 'red', 'stork', 'baseball', 'dream', 'tree', 'crazy', 'soccer',
  'flowers', 'christmas', 'wind', 'wish', 'fall', 'homework', 'puppy', 'bed', 'eyes',
  'fish', 'teacher', 'eat', 'baby', 'moon', 'green', 'shoes', 'beach', 'ice', 'mouse',
  'candy', 'monkey', 'stars', 'heart', 'bear', 'frog', 'hair', 'house', 'people', 'fly',
  'dad', 'food', 'game', 'pizza', 'nature', 'beautiful', 'roses', 'friendship', 'colors',
  'halloween', 'happy', 'animals', 'ocean', 'sports', 'hands', 'pig', 'pie', 'books', 'horse',
  'war', 'monster', 'forever', 'sweet', 'dark', 'ode', 'music', 'water', 'dragon', 'awoke',
  'feet', 'butterfly', 'white', 'hate', 'chicken', 'rat', 'bunny', 'sea', 'hockey',
  'pencil', 'cheese', 'chocolate', 'write', 'car', 'fire', 'dance', 'feelings', 'bananas',
  'pickles', 'angel','kitty', 'weird', 'today', 'rainbow', 'seasons', 'leaves', 'lunch', 'bee',
  'snake', 'birthday', 'computer', 'hat', 'tiger', 'sad', 'earth', 'death', 'money', 'story', 'pink',
  'math', 'magic', 'lion', 'jelly', 'bike', 'america', 'turtle', 'frogs', 'darkness', 'teddy', 'tears',
  'thunder', 'scary']


class ChooseTopic extends Component {

  constructor(props) {
    super(props);
    this.state = { firstSentence: "" };
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  getSample() {
    topics.sample()
  }

  handleChange(e) {
    this.setState({ firstSentence: e.target.value });
  }

  handleSubmit(e) {
    e.preventDefault();
    console.log(this.state.firstSentence);
    fetch(`${server}/generate?${this.state.firstSentence}`, {
      method: 'GET',
      headers: {...headers}
    })
    .then(res => res.json())
    .then((response) => {
      this.props.handleResult(response)
    })
  }

  render() {
    return (
      <div className="WriteSentence">

        <button onClick={this.handleSubmit}>Complete the poem</button>
      </div>
    );
  }
}

export default ChooseTopic;
