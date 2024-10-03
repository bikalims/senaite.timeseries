const path = require("path");
const webpack = require("webpack");
const childProcess = require("child_process");

const BundleAnalyzerPlugin = require("webpack-bundle-analyzer").BundleAnalyzerPlugin;
const CleanCSS = require("clean-css");
const CopyPlugin = require("copy-webpack-plugin");
const CssMinimizerPlugin = require("css-minimizer-webpack-plugin");
const HtmlWebpackPlugin = require("html-webpack-plugin");
const MergeIntoSingleFilePlugin = require("webpack-merge-and-include-globally");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const TerserPlugin = require("terser-webpack-plugin");
const uglifyJS = require("uglify-js");
const { CleanWebpackPlugin } = require("clean-webpack-plugin");


const gitCmd = "git rev-list -1 HEAD -- `pwd`";
let gitHash = childProcess.execSync(gitCmd).toString().substring(0, 7);

const staticPath = path.resolve(__dirname, "../src/senaite/timeseries/browser/static");

const devMode = process.env.mode == "development";
const prodMode = process.env.mode == "production";
const mode = process.env.mode;
console.log(`RUNNING WEBPACK IN '${mode}' MODE`);


module.exports = {
  // https://webpack.js.org/configuration/devtool
  devtool: devMode ? "eval" : "source-map",
  // https://webpack.js.org/configuration/mode/#usage
  mode: mode,
  context: path.resolve(__dirname, "app"),
  entry: {
    "senaite.timeseries": [
      "./senaite.timeseries.js",
      // "./scss/senaite.timeseries.scss"
    ],
  },
  output: {
    // filename: devMode ? "[name].js" : `[name]-${gitHash}.js`,
    filename: "[name].js",
    path: path.resolve(staticPath, "bundles"),
    publicPath: "/++plone++senaite.timeseries.static/bundles"
  },
  module: {
    rules: [
      {
        // Coffee
        test: /\.(coffee)$/,
        exclude: [/node_modules/],
        use: [
          {
            // https://webpack.js.org/loaders/babel-loader/
            loader: "babel-loader"
          },
          {
            // https://webpack.js.org/loaders/coffee-loader/
            loader: "coffee-loader"
          }
        ]
      },
      {
        // JS
        test: /\.(js|jsx)$/,
        exclude: [/node_modules/],
        use: [
          {
            // https://webpack.js.org/loaders/babel-loader/
            loader: "babel-loader"
          }
        ]
      },
      {
        // SCSS
        test: /\.s[ac]ss$/i,
        use: [
          {
            // https://webpack.js.org/plugins/mini-css-extract-plugin/
            loader: MiniCssExtractPlugin.loader,
          },
          {
            // https://webpack.js.org/loaders/css-loader/
            loader: "css-loader"
          },
          {
            // https://webpack.js.org/loaders/sass-loader/
            loader: "sass-loader"
          }
        ]
      },
      {
        test: /\.(png|jpg)(\?v=\d+\.\d+\.\d+)?$/,
        use: [
          {
            // https://webpack.js.org/loaders/file-loader/
            loader: "file-loader",
            options: {
              name: "[name].[ext]",
              outputPath: "../assets/img",
              publicPath: "/++plone++senaite.timeseries.static/assets/img",
            }
          }
        ]
      }
    ]
  },
  optimization: {
    minimize: prodMode,
    minimizer: [
      // https://v4.webpack.js.org/plugins/terser-webpack-plugin/
      new TerserPlugin({
        exclude: /\/modules/,
        terserOptions: {
          // https://github.com/webpack-contrib/terser-webpack-plugin#terseroptions
          sourceMap: false, // Must be set to true if using source-maps in production
          format: {
            comments: false
          },
          compress: {
            drop_console: true,
            passes: 2,
          },
	      }
      }),
      // https://webpack.js.org/plugins/css-minimizer-webpack-plugin/
      new CssMinimizerPlugin({
        exclude: /\/modules/,
        minimizerOptions: {
          preset: [
            "default",
            {
              discardComments: { removeAll: true },
            },
          ],
        },
      }),
    ],
  },
  plugins: [
    // https://github.com/johnagan/clean-webpack-plugin
    new CleanWebpackPlugin(),
    // https://webpack.js.org/plugins/html-webpack-plugin/
    new HtmlWebpackPlugin({
      inject: false,
      filename:  path.resolve(staticPath, "resources.pt"),
      template: "resources.pt",
    }),
    // https://webpack.js.org/plugins/mini-css-extract-plugin/
    new MiniCssExtractPlugin({
      filename: devMode ? "[name].css" : "[name].[hash].css",
      chunkFilename: devMode ? "[id].css" : "[id].[hash].css",
    }),
    // https://webpack.js.org/plugins/copy-webpack-plugin/
    // new CopyPlugin({
    //   patterns: [
    //   ]
    // }),
    // https://webpack.js.org/plugins/provide-plugin/
    new webpack.ProvidePlugin({
      $: "jquery",
      jQuery: "jquery",
    }),
  ],
  externals: {
    // https://webpack.js.org/configuration/externals
    react: "React",
    "react-dom": "ReactDOM",
    $: "jQuery",
    jquery: "jQuery",
    bootstrap: "bootstrap",
    tinyMCE: "tinymce"
  },
resolve: {
  alias: {
    'app/components/TableCell': path.resolve(__dirname, 'app/components/TableCell.coffee'),
    'app/components/Checkbox': path.resolve(__dirname, '../senaite.app.listing/webpack/app/components/Checkbox.coffee'),
    'app/components/HiddenField': path.resolve(__dirname, '../senaite.app.listing/webpack/app/components/HiddenField.coffee'),
    'app/components/MultiChoice': path.resolve(__dirname, '../senaite.app.listing/webpack/app/components/MultiChoice.coffee'),
    'app/components/MultiSelect': path.resolve(__dirname, '../senaite.app.listing/webpack/app/components/MultiSelect.coffee'),
    'app/components/MultiValue': path.resolve(__dirname, '../senaite.app.listing/webpack/app/components/MultiValue.coffee'),
    'app/components/NumericField': path.resolve(__dirname, '../senaite.app.listing/webpack/app/components/NumericField.coffee'),
    'app/components/CalculatedField': path.resolve(__dirname, '../senaite.app.listing/webpack/app/components/CalculatedField.coffee'),
    'app/components/ReadonlyField': path.resolve(__dirname, '../senaite.app.listing/webpack/app/components/ReadonlyField.coffee'),
    'app/components/Select': path.resolve(__dirname, '../senaite.app.listing/webpack/app/components/Select.coffee'),
    'app/components/StringField': path.resolve(__dirname, '../senaite.app.listing/webpack/app/components/StringField.coffee'),
    'app/components/TextField': path.resolve(__dirname, '../senaite.app.listing/webpack/app/components/TextField.coffee'),
    'app/components/FractionField': path.resolve(__dirname, '../senaite.app.listing/webpack/app/components/FractionField.coffee'),
    'app/components/DateTime': path.resolve(__dirname, '../senaite.app.listing/webpack/app/components/DateTime.coffee'),
    // Add more aliases as needed for other dependencies
  },
  extensions: ['.js', '.jsx', '.coffee'],
}

};
