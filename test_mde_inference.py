#!/usr/bin/env python3
# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license
"""Test script for MDE inference and metrics functionality."""

import os
import sys

import torch


def test_depth_metrics():
    """Test the depth metrics functions."""
    print("🧪 Testing depth metrics...")

    try:
        from ultralytics.utils.metrics_mde import (
            calculate_absolute_depth_error,
            calculate_depth_accuracy,
            calculate_depth_error,
            calculate_squared_depth_error,
            print_depth_statistics,
        )

        # Create test data
        pred_depths = torch.tensor([10.0, 20.0, 30.0, 40.0, 50.0])
        gt_depths = torch.tensor([12.0, 18.0, 32.0, 38.0, 52.0])

        # Test depth error rate
        error_rate = calculate_depth_error(pred_depths, gt_depths)
        print(f"   ✅ Depth error rate: {error_rate:.2f}%")

        # Test absolute error
        abs_error = calculate_absolute_depth_error(pred_depths, gt_depths)
        print(f"   ✅ Absolute error: {abs_error:.2f}m")

        # Test squared error (RMSE)
        rmse = calculate_squared_depth_error(pred_depths, gt_depths)
        print(f"   ✅ RMSE: {rmse:.2f}m")

        # Test accuracy metrics
        acc_metrics = calculate_depth_accuracy(pred_depths, gt_depths)
        print(f"   ✅ Accuracy metrics: {acc_metrics}")

        # Test depth statistics
        print_depth_statistics(pred_depths, "Test Predictions")

        return True

    except Exception as e:
        print(f"   ❌ Error testing metrics: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_inference_functionality():
    """Test the inference functionality."""
    print("\n🧪 Testing inference functionality...")

    try:
        from ultralytics import YOLO

        # Test loading the MDE model
        model = YOLO("ultralytics/cfg/models/11/yolo11-mde.yaml")
        print("   ✅ MDE model loaded successfully!")

        # Test forward pass
        dummy_input = torch.randn(1, 3, 640, 640)
        with torch.no_grad():
            outputs = model.model(dummy_input)

        print(f"   ✅ Forward pass successful! Output type: {type(outputs)}")

        # Test Detect_MDE head
        last_layer = model.model[-1]
        if hasattr(last_layer, "cv_depth"):
            print("   ✅ Detect_MDE head with depth branch detected!")
        else:
            print("   ❌ Detect_MDE head not found!")
            return False

        return True

    except Exception as e:
        print(f"   ❌ Error testing inference: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_training_script():
    """Test the training script functionality."""
    print("\n🧪 Testing training script...")

    try:
        # Test importing the training script
        sys.path.append("/root/ultralytics/examples")
        from train_yolo11_mde import evaluate_mde_model, predict_with_depth

        print("   ✅ Training script functions imported successfully!")

        # Test function signatures
        import inspect

        # Check predict_with_depth signature
        sig = inspect.signature(predict_with_depth)
        params = list(sig.parameters.keys())
        if "model" in params and "image_path" in params:
            print("   ✅ predict_with_depth function signature correct!")
        else:
            print(f"   ❌ predict_with_depth signature incorrect: {params}")
            return False

        # Check evaluate_mde_model signature
        sig = inspect.signature(evaluate_mde_model)
        params = list(sig.parameters.keys())
        if "model_path" in params and "data_path" in params:
            print("   ✅ evaluate_mde_model function signature correct!")
        else:
            print(f"   ❌ evaluate_mde_model signature incorrect: {params}")
            return False

        return True

    except Exception as e:
        print(f"   ❌ Error testing training script: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_dataset_access():
    """Test access to the prepared dataset."""
    print("\n🧪 Testing dataset access...")

    try:
        dataset_path = "/root/autodl-tmp/kitti_yolo_depth"

        if not os.path.exists(dataset_path):
            print(f"   ❌ Dataset path not found: {dataset_path}")
            return False

        # Check for images and labels
        images_path = os.path.join(dataset_path, "images")
        labels_path = os.path.join(dataset_path, "labels")

        if not os.path.exists(images_path):
            print(f"   ❌ Images directory not found: {images_path}")
            return False

        if not os.path.exists(labels_path):
            print(f"   ❌ Labels directory not found: {labels_path}")
            return False

        # Count files
        import glob

        num_images = len(glob.glob(os.path.join(images_path, "*.png")))
        num_labels = len(glob.glob(os.path.join(labels_path, "*.txt")))

        print(f"   ✅ Dataset found: {num_images} images, {num_labels} labels")

        if num_images > 0 and num_labels > 0:
            print("   ✅ Dataset is ready for training!")
            return True
        else:
            print("   ❌ Dataset is empty!")
            return False

    except Exception as e:
        print(f"   ❌ Error testing dataset: {e}")
        import traceback

        traceback.print_exc()
        return False


def main():
    """Run all inference and metrics tests."""
    print("=" * 60)
    print("🎯 MDE Inference and Metrics Test")
    print("=" * 60)

    success = True

    # Run tests
    success &= test_depth_metrics()
    success &= test_inference_functionality()
    success &= test_training_script()
    success &= test_dataset_access()

    print("\n" + "=" * 60)
    if success:
        print("🏁 All inference and metrics tests passed!")
        print("=" * 60)
        print("\n📋 Ready for MDE inference and evaluation!")
        print("\n🚀 Usage examples:")
        print("   # Train the model")
        print("   python examples/train_yolo11_mde.py train")
        print("\n   # Evaluate with depth metrics")
        print("   python examples/train_yolo11_mde.py eval")
        print("\n   # Run inference")
        print("   python examples/train_yolo11_mde.py predict")
    else:
        print("❌ Some tests failed!")
        print("=" * 60)

    return success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
