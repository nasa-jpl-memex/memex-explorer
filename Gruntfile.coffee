module.exports = (grunt) ->
  grunt.loadNpmTasks('grunt-contrib-coffee')
  grunt.loadNpmTasks('grunt-contrib-watch')

  grunt.initConfig
    watch:
      coffee:
        files: 'app/static/coffee/*.coffee'
        tasks: ['coffee:compile']

    coffee:
      compile:
        options:
          bare: true
        expand: true,
        flatten: false,
        cwd: "#{__dirname}/app/static/coffee/",
        src: ['*.coffee'],
        dest: 'app/static/js',
        ext: '.js'

    eco:
      files:
        expand: true,
        flatten: false,
        cwd: "#{__dirname}/app/static/coffee/",
        src: ['*.eco'],
        dest: 'app/static/js',
        ext: '.js'