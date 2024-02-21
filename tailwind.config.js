/** @type {import('tailwindcss').Config} */
module.exports = {
  mode: 'jit',
  content: [
    "./templates/**/*.html",
    "./static/js/**/*.js",
  ],
  theme: {
    extend: {
      boxShadow: {
        'neon-purple': '0 0 10px #D946EF, 0 0 20px #D946EF, 0 0 30px #D946EF',
      }
    },
  },
  plugins: [],
}

