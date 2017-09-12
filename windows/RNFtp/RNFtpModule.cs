using ReactNative.Bridge;
using System;
using System.Collections.Generic;
using Windows.ApplicationModel.Core;
using Windows.UI.Core;

namespace Com.Reactlibrary.RNFtp
{
    /// <summary>
    /// A module that allows JS to share data.
    /// </summary>
    class RNFtpModule : NativeModuleBase
    {
        /// <summary>
        /// Instantiates the <see cref="RNFtpModule"/>.
        /// </summary>
        internal RNFtpModule()
        {

        }

        /// <summary>
        /// The name of the native module.
        /// </summary>
        public override string Name
        {
            get
            {
                return "RNFtp";
            }
        }
    }
}
