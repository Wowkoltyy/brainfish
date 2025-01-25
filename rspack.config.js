const path = require('path');
const rspack = require('@rspack/core');

module.exports = {
  entry: {
    popup: './src/popup.ts',
    background: './src/background.ts'
  },
  output: {
    filename: '[name].js',
    path: path.resolve(__dirname, 'dist'),
  },
  module: {
    rules: [
      {
        test: /\.svelte$/,
        use: {
          loader: 'svelte-loader',
          options: {
            emitCss: true,
            hotReload: true
          }
        }
      },
      {
        test: /\.css$/,
        use: [
          'style-loader',
          'css-loader',
          'postcss-loader'
        ]
      }
    ]
  },
  resolve: {
    extensions: ['.mjs', '.js', '.svelte']
  },
  plugins: [
    new rspack.CopyRspackPlugin({
        patterns: [
          { from: "manifest.json", to: "manifest.json" },
          { from: "popup.html", to: "popup.html" },
        ],
      }),
  ],
};