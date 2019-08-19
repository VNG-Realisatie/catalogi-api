const gulp = require('gulp');
const { scss } = require('./scss');

const build = gulp.parallel(scss);

gulp.task('build', build);
exports.build = build;
