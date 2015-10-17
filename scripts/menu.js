"use strict";

var fs = require('fs');
var util = require('util');
var path = require('path');
var _ = require("underscore");
var colors = require('colors');
var progress = require('progress');
var inquirer = require("inquirer");
var exec = require('child_process').exec;

var years = [
	{
		name: '2011'
	},
	{
		name: '2012'
	},
	{
		name: '2013'
	},
	{
		name: '2014'
	},
	{
		name: '2015',
		checked: true
	}
]

var transformers = [
	{
		'name': 'StandardGameTransformer',
		checked: true
  },
  {
		'name': 'StandardPlayerTransformer',
		checked: false
  },
	{
		'name': 'PlayerVectorizerTransformer'
	}
]

console.log()
console.log("Loaded ".yellow.bold + transformers.length.toString().underline.bold.yellow + " transformers...".yellow.bold);
console.log()

inquirer.prompt([
	{
		type: "list",
		message: "What would you like to do?",
		name: "action",
		choices: ["Generate Dataset"]
  },
	{
		type: "checkbox",
		message: "Select transformers to evaluate:",
		name: "transformers",
		choices: transformers,
		validate: function (answer) {
			if (answer.length < 1) {
				return "You must choose at least one transformer!";
			}
			return true;
		},
		when: function (answer) {
			return answer.action == "Generate Dataset"
		},
	},
	{
		type: "checkbox",
		message: "Select years to evaluate:",
		name: "years",
		choices: years,
		validate: function (answer) {
			if (answer.length < 1) {
				return "You must choose at least one year!";
			}
			return true;
		},
		when: function (answer) {
			return answer.action == "Generate Dataset"
		}
  }
], function (answers) {
  console.log()
  console.log()
  if (answers.action == "Generate Dataset") {
		var years_string = ""
		for (var i = 0; i < answers.years.length; i++) {
			years_string += (answers.years[i] + " ")
		}

		var bar = new progress('Running transformers [:bar] :percent ETA: :etas', {
      total: answers.transformers.length,
      width: 20
    });

    var update_data_file = path.join(__dirname, "run-transformer.py");
    for (var i = 0; i < answers.transformers.length; i++) {
      exec('python '+update_data_file+' '+answers.transformers[i]+' --years '+years_string, function (error, stdout, stderr){
        bar.tick();
				if (stdout) console.log(stdout)
				if (stderr)	console.log(stderr.red)
      });
    }
  }
});
