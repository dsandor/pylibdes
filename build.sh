#!/bin/bash

# Build script for DES Lambda container supporting both amd64 and arm64

set -e

# Default values
IMAGE_NAME="libdes-lambda"
TAG="latest"
PLATFORMS="linux/amd64,linux/arm64"

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --image-name)
            IMAGE_NAME="$2"
            shift 2
            ;;
        --tag)
            TAG="$2"
            shift 2
            ;;
        --platforms)
            PLATFORMS="$2"
            shift 2
            ;;
        --help)
            echo "Usage: $0 [--image-name NAME] [--tag TAG] [--platforms PLATFORMS]"
            echo "  --image-name: Docker image name (default: libdes-lambda)"
            echo "  --tag: Docker image tag (default: latest)"
            echo "  --platforms: Comma-separated list of platforms (default: linux/amd64,linux/arm64)"
            echo "  --help: Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

echo "Building DES Lambda container..."
echo "Image: ${IMAGE_NAME}:${TAG}"
echo "Platforms: ${PLATFORMS}"

# Ensure buildx is available
if ! docker buildx version >/dev/null 2>&1; then
    echo "Error: docker buildx is not available. Please install Docker with buildx support."
    exit 1
fi

# Create a new builder instance if it doesn't exist
BUILDER_NAME="libdes-builder"
if ! docker buildx inspect $BUILDER_NAME >/dev/null 2>&1; then
    echo "Creating buildx builder: $BUILDER_NAME"
    docker buildx create --name $BUILDER_NAME --use
fi

# Use the builder
docker buildx use $BUILDER_NAME

# Build the image for multiple platforms
docker buildx build \
    --platform $PLATFORMS \
    --tag ${IMAGE_NAME}:${TAG} \
    --push \
    .

echo "Build completed successfully!"
echo "Image: ${IMAGE_NAME}:${TAG}"
echo "Platforms: ${PLATFORMS}" 