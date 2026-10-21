#!/bin/sh
# Builds the offline NuGet cache tarball (Source1) for the filee spec.
# Run on a machine with network access and dotnet-sdk-10.0 installed.
#   ./make-nuget-cache.sh 2.0.0
# Then:  abb store filee-2.0.0-nuget-packages.tar.zst   (and Filee-2.0.0.tar.gz)
set -eu
ver="${1:?usage: $0 VERSION}"
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT

git clone --depth 1 --branch "v$ver" https://github.com/KnifeLemon/Filee "$work/src"
cd "$work/src"

export DOTNET_CLI_TELEMETRY_OPTOUT=1 DOTNET_NOLOGO=1
export NUGET_PACKAGES="$work/nuget-packages"

# Restore for every RID/project the spec publishes so runtime-specific native
# assets (SkiaSharp, HarfBuzz, libuiohook) are in the cache for both arches.
for rid in linux-x64 linux-arm64; do
  for p in Filee.App Filee.Cli; do
    dotnet restore "src/$p/$p.csproj" -r "$rid"
  done
done

# The publish step also needs the apphost / runtime packs for each RID.
for rid in linux-x64 linux-arm64; do
  for p in Filee.App Filee.Cli; do
    dotnet publish "src/$p/$p.csproj" -c Release -r "$rid" --self-contained false \
      -p:PublishReadyToRun=false -o "$work/discard-$rid-$p" >/dev/null
  done
done

tar -C "$work/nuget-packages" --zstd -cf "$OLDPWD/filee-$ver-nuget-packages.tar.zst" .
echo "Wrote filee-$ver-nuget-packages.tar.zst"
