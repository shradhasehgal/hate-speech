import React, { Component } from 'react';
import './App.css';
import * as d3 from 'd3';
import counts from './counts_data.csv';
import hashtags from './hashtags_data.csv';

class App extends Component {

    constructor(props) {
        super(props)
        this.state = {
            count: [],
            hashtag: [],
            category: ""
        }
        this.handleChangeCategory = this.handleChangeCategory.bind(this);
    }

    componentDidMount() {
        var that = this;
        // Load tweet count for hate classes
        d3.csv(counts)
            .then(function (countData) {
                console.log(countData)
                // Load hashtags for hate classes
                d3.csv(hashtags)
                    .then(function (hashtagData) {
                        console.log(hashtagData);
                        // Setting state with precomputed data from csv files
                        that.setState({ count: countData, hashtag: hashtagData });
                    })
                    .catch(function (err) {
                        throw err;
                    })
            })
            .catch(function (err) {
                throw err;
            })
    }

    handleChangeCategory(event) {
        this.setState({ category: event.target.value });
    }

    render() {

        return (
            <div className="App" >
                <br />
                <h1>Twitter Hate Speech</h1>
                <form>
                    <div class="form-group assign">
                        <select value={this.state.category} class="form-control" onChange={this.handleChangeCategory}>
                            <option disabled value="">Choose category</option>
                            <option value="racism">Racism</option>
                            <option value="sexism">Sexism</option>
                            <option value="none">None</option>
                        </select>
                        <br />
                    </div>
                </form>
                <br />

                {this.state.count.map((obj, index) => {
                    // Display count of tweets associated with chosen category
                    return obj.category === this.state.category ?
                        <div>
                            <h2>Count of tweets belonging to class '{this.state.category}'</h2>
                            <p>{obj.count}</p>
                        </div>
                        : ''
                })}
                {
                    this.state.category !== "" ? <h2>Associated Hashtags</h2> : ''
                }
                {this.state.hashtag.map((obj, index) => {
                    // Display hashtags associated with chosen category
                    return obj.category === this.state.category ?
                        <div>
                            <p>#{obj.hashtag}</p>
                        </div>
                        : ''

                })}
            </div>
        );
    }
}

export default App;
