{pkgs ? import <nixpkgs> {}}:
pkgs.mkShell {
  buildInputs = with pkgs; [
    # Python and pip
    python3
    python3Packages.pip
    python3Packages.virtualenv

    # Playwright dependencies
    python3Packages.playwright

    # System dependencies needed for Playwright browsers
    chromium

    # Additional system libraries that Playwright needs
    glib
    nss
    nspr
    at-spi2-atk
    cups
    gtk3
    pango
    cairo
    xorg.libX11
    xorg.libXcomposite
    xorg.libXdamage
    xorg.libXext
    xorg.libXfixes
    xorg.libXrandr
    xorg.libxcb
    libxkbcommon
    alsa-lib
    at-spi2-core
    dbus
    expat
    fontconfig
    freetype
    gdk-pixbuf
    mesa
    vulkan-loader
    udev
    libdrm

    # Additional libraries from the error message
    gobject-introspection
    atk

    # Additional packages for better browser support
    xvfb-run
    libGL

    # Additional mesa components for libgbm
    wayland
  ];

  shellHook = ''
    echo "Python environment with Playwright ready!"
    echo "Available Python version: $(python --version)"
    echo ""
    echo "To install Playwright browsers, run:"
    echo "  playwright install chromium"
    echo ""
    echo "To generate screenshots, run:"
    echo "  python screenshot_generator.py"
    echo ""

    # Set environment variables for Playwright
    export PLAYWRIGHT_BROWSERS_PATH="$HOME/.cache/ms-playwright"
    export PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1
    export PLAYWRIGHT_SKIP_VALIDATE_HOST_REQUIREMENTS=1

    # Help Playwright find system libraries
    export LD_LIBRARY_PATH="${pkgs.lib.makeLibraryPath [
      pkgs.glib
      pkgs.nss
      pkgs.nspr
      pkgs.at-spi2-atk
      pkgs.cups
      pkgs.gtk3
      pkgs.pango
      pkgs.cairo
      pkgs.xorg.libX11
      pkgs.xorg.libXcomposite
      pkgs.xorg.libXdamage
      pkgs.xorg.libXext
      pkgs.xorg.libXfixes
      pkgs.xorg.libXrandr
      pkgs.xorg.libxcb
      pkgs.libxkbcommon
      pkgs.alsa-lib
      pkgs.at-spi2-core
      pkgs.dbus
      pkgs.expat
      pkgs.udev
      pkgs.libdrm
      pkgs.mesa
      pkgs.wayland
      pkgs.libGL
      pkgs.gobject-introspection
      pkgs.atk
    ]}:$LD_LIBRARY_PATH"

    # Use system browsers if available
    export PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH="${pkgs.chromium}/bin/chromium"

    # Additional environment variables for graphics
    export DISPLAY=:0
    export LIBGL_DRIVERS_PATH="${pkgs.mesa}/lib/dri"
    export __GL_SHADER_DISK_CACHE_PATH="/tmp"
  '';
}
