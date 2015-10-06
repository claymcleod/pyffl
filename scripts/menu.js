"use strict";

var fs = require('fs');
var util = require('util');
var path = require('path');
var _ = require("underscore");
var colors = require('colors');
var progress = require('progress');
var inquirer = require("inquirer");
var exec = require('child_process').exec;

var transformers = [
	{
		'name': 'StandardGameTransformer',
		checked: true
  },
  {
		'name': 'StandardPlayerTransfomer',
		checked: false
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
		choices: ["Generate Dataset", "Classify"]
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
		}
  }
], function (answers) {
  console.log()
  console.log()
  if (answers.action == "Generate Dataset") {
    var bar = new progress('Running transformers [:bar] :percent ETA: :etas', {
      total: answers.transformers.length,
      width: 20
    });

    var update_data_file = path.join(__dirname, "update-data.py");
    for (var i = 0; i < answers.transformers.length; i++) {
      exec('python '+update_data_file+' '+answers.transformers[i], function (error, stdout, stderr){
        bar.tick();
      });
    }
  }
});
