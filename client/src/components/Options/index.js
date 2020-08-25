import React, { Component } from 'react';

import './styles.css';

class Options extends Component {
  constructor(props) {
    super(props);
    this.onWriteSentence = this.onWriteSentence.bind(this);
    this.onChooseTopic = this.onChooseTopic.bind(this);
  }

  onWriteSentence() {
    this.props.handleOptions("writeSentence");
  }

  onChooseTopic() {
    this.props.handleOptions("chooseTopic");
  }

  render() {
    return (
      <div className="Options">
          <button onClick={this.onWriteSentence}>Write your first sentence</button>
          <button onClick={this.onChooseTopic}>Choose a topic</button>
      </div>
    );
  }
}

export default Options;
