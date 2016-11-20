var React = require('react');
var ReactDom = require('react-dom');
var Jxau = require('./components/Jxau');

console.log(ReactDom);
console.log(Jxau);

ReactDom.render(<Jxau />, document.getElementById('jxau-container'));
