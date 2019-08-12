const gulp = require('gulp');
const paths = require('../paths');
const {scss} = require('./scss');


/**
 * Watch task
 * Run using "gulp watch"
 * Runs "watch-js" and "watch-sass" tasks
 */
const watch = gulp.parallel(watchSCSS);

/**
 * Watch-sass task
 * Run using "gulp watch-scss"
 * Runs "sass" task instantly and when any file in paths.sassSrc changes
 */
function watchSCSS() {
    scss()
    gulp.watch(paths.sassSrc, scss);
}



exports.watch = watch;
gulp.task('watch', watch);


exports.watchSCSS = watchSCSS;
gulp.task('watch-scss', watchSCSS);
