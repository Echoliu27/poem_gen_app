import React, { Component } from 'react';

import './styles.css';

const server = "http://104.154.101.183:5000"
const headers = {
  'Accept': 'application/json'
}

class ChooseTopic extends Component {

  constructor(props) {
    super(props);
    this.state = { firstSentence: "" };
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
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
