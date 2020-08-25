import React, { Component } from 'react';

import './styles.css';

class Result extends Component {

  render() {
    return (
      <div className="Title">
        <h4>{this.props.generatedPoem}</h4>
        <button onClick={this.props.resetPage}>Try another one</button>
      </div>
    );
  }
}

export default Result;
