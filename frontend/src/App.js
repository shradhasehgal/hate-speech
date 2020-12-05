import logo from './logo.svg';
import React, {Component} from 'react';
import './App.css';
import * as d3 from 'd3';
import counts from './counts_data.csv';
import hashtags from './hashtags_data.csv';

class App extends Component {

  constructor(props) {
      super(props)
  }
  
  componentDidMount() {
  
      d3.csv(counts)
      .then(function(count) {
          console.log(count)
          d3.csv(hashtags)
          .then(function(hashtag){
              console.log(hashtag);
              this.setState({count: count, hashtag: hashtag});
          })
          .catch(function(err){
              throw err;
          })
      })
      .catch(function(err) {
          throw err;
      })
  }
  
  render() {
  
      return ( 
               <div className = "App" >
                <div> Data Visualization </div> 
                {this.state.count.map((category, index) => (
        <p>{category.name} from {person.country}!</p>))}
               </div>
          );
      }
}

export default App;
