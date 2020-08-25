import React, { Component } from 'react';

import './styles.css';

const server = "http://104.154.101.183:5000"
const headers = {
  'Accept': 'application/json'
}

class WriteSentence extends Component {

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
    fetch(`${server}/generate?firstLine=${this.state.firstSentence}`, {
      method: 'GET',
      headers: {...headers}
    })
    .then(res => res.json())
    .then((response) => {
      this.props.handleResult(response);
    })
  }

  render() {
    return (
      <div className="WriteSentence">
        <h3>Write your first sentence...</h3>
        <input id="first sentence" onChange={this.handleChange} value={this.state.firstSentence} />
        <button onClick={this.handleSubmit}>Complete the poem</button>
      </div>
    );
  }
}

export default WriteSentence;
