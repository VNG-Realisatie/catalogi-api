'use strict';
var gulp = require('gulp');
var jshint = require('gulp-jshint');
var paths = require('../paths');


/**
 * Lint task
 * Run using "gulp lint"
 * Runs jshint
 */
gulp.task('lint', function() {
    return gulp.src([paths.jsSrc, paths.jsSpec])
        .pipe(jshint())
        .pipe(jshint.reporter('default'))
});
