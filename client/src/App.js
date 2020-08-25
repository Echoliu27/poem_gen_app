import React, { Component } from 'react';

import header from './img/header.png';
import footer from './img/footer.png';
import './App.css';

import Title from './components/Title/index.js';
import Options from './components/Options/index.js';
import WriteSentence from './components/WriteSentence/index.js';
import ChooseTopic from './components/ChooseTopic/index.js';
import Result from './components/Result/index.js';


class App extends Component {
  constructor() {
    super();
    this.state = {
      showOptions: true,
      showWriteSentence: false,
      showChooseTopic: false,
      showResult: false,
      generatedPoem: ""
    };

    this.resetPage = this.resetPage.bind(this);
    this.handleOptions = this.handleOptions.bind(this);
    this.handleResult = this.handleResult.bind(this);
  }

  resetPage() {
    this.setState({
      showOptions: true,
      showWriteSentence: false,
      showChooseTopic: false,
      showResult: false,
      generatedPoem: ""
    })
  }

  handleOptions(option) {
    if (option === "writeSentence") {
      this.setState({
        showOptions: false,
        showWriteSentence: true
      })
    }
    if (option === "chooseTopic") {
      this.setState({
        showOptions: false,
        showChooseTopic: true
      })
    }
  }

  handleResult(result) {
    console.log(result);
    this.setState({
      showWriteSentence: false,
      showChooseTopic: false,
      showResult: true,
      generatedPoem: result["data"]
    })
  }

  render() {
    const { showOptions, showWriteSentence, showChooseTopic, showResult } = this.state;
    return (
      <div className="App">
        <img src={header} className="App-logo" alt="logo" />
        <Title />
        {showOptions && <Options handleOptions={this.handleOptions} />}
        {showWriteSentence && <WriteSentence handleResult={this.handleResult} />}
        {showChooseTopic && <ChooseTopic handleResult={this.handleResult} />}
        {showResult && <Result generatedPoem={this.state.generatedPoem} resetPage={this.resetPage} />}
        <img src={footer} className="App-logo" alt="logo" />
      </div>
    );
  }
}

export default App;
