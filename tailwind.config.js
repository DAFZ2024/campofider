/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "./templates/**/*.html",
        "./admin/**/*.html",
        "./static/**/*.js",
    ],
    theme: {
        extend: {
            colors: {
                primary: {
                    50: '#f0fdf4',
                    100: '#dcfce7',
                    200: '#b9f8cf',
                    300: '#7bf1a8',
                    400: '#05df72',
                    500: '#00c950',
                    600: '#00a63e',
                    700: '#008236',
                    800: '#016630',
                    900: '#0d542b',
                    950: '#032e15',
                },
            },
        },
    },
    plugins: [],
}
