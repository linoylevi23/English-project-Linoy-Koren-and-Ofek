"""
ex_neural_network.py
עבודה מספר 1: רשתות נוירונים עמוקות עבור מאגר Oxford-IIIT Pet Dataset.
סעיף א': בניית רשת נוירונים עמוקה (DNN) ובדיקת כמות הפרמטרים שלה.
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import tensorflow_datasets as tfds
import matplotlib.pyplot as plt
import numpy as np

# הגדרת קבועים
IMG_SIZE = 128
BATCH_SIZE = 64
SHUFFLE_BUFFER = 1000


def preprocess(image, label, img_size=IMG_SIZE):
    """
    עיבוד מקדים: שינוי גודל התמונה ונרמול ערכי הפיקסלים לטווח [0.0, 1.0].
    """
    image = tf.image.resize(image, (img_size, img_size))
    image = tf.cast(image, tf.float32) / 255.0
    return image, label


def load_oxford_pets(img_size=IMG_SIZE, batch_size=BATCH_SIZE):
    """
    טעינת המאגר Oxford-IIIT Pet דרך TensorFlow Datasets והכנת צינור הנתונים (tf.data).
    """
    (ds_train, ds_test), ds_info = tfds.load(
        'oxford_iiit_pet:3.*.*',
        split=['train', 'test'],
        as_supervised=True,
        with_info=True
    )

    num_classes = ds_info.features['label'].num_classes

    # צינור נתוני אימון: מיפוי -> ערבוב -> קיבוץ למנות (batches) -> טעינה מקדימה (prefetch)
    train_data = (
        ds_train
        .map(lambda img, lbl: preprocess(img, lbl, img_size), num_parallel_calls=tf.data.AUTOTUNE)
        .shuffle(buffer_size=SHUFFLE_BUFFER)
        .batch(batch_size)
        .prefetch(buffer_size=tf.data.AUTOTUNE)
    )

    # צינור נתוני בדיקה
    test_data = (
        ds_test
        .map(lambda img, lbl: preprocess(img, lbl, img_size), num_parallel_calls=tf.data.AUTOTUNE)
        .batch(batch_size)
        .prefetch(buffer_size=tf.data.AUTOTUNE)
    )

    return train_data, test_data, ds_info, num_classes


def build_dnn_model(input_shape=(IMG_SIZE, IMG_SIZE, 3), num_classes=37):
    """
    סעיף א': יצירת רשת נוירונים עמוקה (DNN - Deep Neural Network / Fully Connected).
    הרשת מקבלת תמונה בגודל (IMG_SIZE, IMG_SIZE, 3), משטחת אותה (Flatten)
    לוקטור חד-ממדי (128x128x3 = 49,152 כניסות), ולאחר מכן עוברת דרך שכבות Dense עמוקות
    עם אקטיבציית ReLU, שכבות BatchNormalization ו-Dropout למניעת Overfitting,
    ולבסוף שכבת Dense של 37 נוירונים עם Softmax לסיווג.
    """
    model = keras.Sequential([
        # שכבת שיטוח (Flatten) של התמונה
        layers.Flatten(input_shape=input_shape, name="flatten_input"),
        
        # שכבה מוסתרת ראשונה: 512 נוירונים
        layers.Dense(512, activation="relu", name="dense_1"),
        layers.BatchNormalization(name="bn_1"),
        layers.Dropout(0.3, name="dropout_1"),
        
        # שכבה מוסתרת שנייה: 256 נוירונים
        layers.Dense(256, activation="relu", name="dense_2"),
        layers.BatchNormalization(name="bn_2"),
        layers.Dropout(0.3, name="dropout_2"),
        
        # שכבה מוסתרת שלישית: 128 נוירונים
        layers.Dense(128, activation="relu", name="dense_3"),
        
        # שכבת פלט: 37 מחלקות עם פונקציית סופטמקס (Softmax)
        layers.Dense(num_classes, activation="softmax", name="output_layer")
    ], name="OxfordPets_DNN_Model")

    # קומפילציה לרשת
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss=keras.losses.SparseCategoricalCrossentropy(),
        metrics=["accuracy"]
    )

    return model


def show_samples(dataset, class_names=None, num_samples=9):
    """
    הצגת דוגמאות מתוך המאגר יחד עם התוויות שלהן.
    """
    for images, labels in dataset.take(1):
        plt.figure(figsize=(9, 9))
        for i in range(min(num_samples, len(images))):
            ax = plt.subplot(3, 3, i + 1)
            plt.imshow(images[i].numpy())
            label_idx = int(labels[i].numpy())
            title = class_names[label_idx] if class_names else f"Class: {label_idx}"
            plt.title(title, fontsize=9)
            plt.axis("off")
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    print(f"TensorFlow Version: {tf.__version__}")

    # טעינת נתונים
    train_data, test_data, ds_info, num_classes = load_oxford_pets(
        img_size=IMG_SIZE,
        batch_size=BATCH_SIZE
    )

    print(f"Number of classes: {num_classes}")
    print(f"Train split size: {ds_info.splits['train'].num_examples} samples")
    print(f"Test split size:  {ds_info.splits['test'].num_examples} samples")

    # =========================================================================
    # סעיף א': בניית רשת נוירונים עמוקה (DNN) ובדיקת כמות הפרמטרים
    # =========================================================================
    print("\n" + "=" * 65)
    print("סעיף א': בניית רשת נוירונים עמוקה (DNN) ובדיקת כמות הפרמטרים")
    print("=" * 65)

    model = build_dnn_model(
        input_shape=(IMG_SIZE, IMG_SIZE, 3),
        num_classes=num_classes
    )

    # הדפסת ארכיטקטורת הרשת וטבלת הפרמטרים המלאה (Layer by Layer)
    model.summary()

    # חישוב והצגת כמות הפרמטרים
    total_params = model.count_params()
    trainable_params = sum(tf.keras.backend.count_params(w) for w in model.trainable_weights)
    non_trainable_params = sum(tf.keras.backend.count_params(w) for w in model.non_trainable_weights)

    print("\n" + "-" * 45)
    print(f"סה\"כ פרמטרים ברשת (Total Params):          {total_params:,}")
    print(f"פרמטרים לאימון (Trainable Params):         {trainable_params:,}")
    print(f"פרמטרים שאינם לאימון (Non-Trainable):      {non_trainable_params:,}")
    print("-" * 45 + "\n")
