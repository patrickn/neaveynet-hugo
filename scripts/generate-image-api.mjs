import { readdir, writeFile, stat } from "fs/promises";
import { join, relative } from "path";

import exifr from 'exifr';
const { parse } = exifr;

const imageDir = "static/img";
const functionDir = "netlify/functions";
const functionFile = join(functionDir, "image-api.mjs");

const IMAGE_EXTENSIONS_REGEX = /\.(jpg|jpeg|png)$/i;

async function getImagesRecursive(dir) {
  let images = [];

  try {
    const files = await readdir(dir);

    for (const file of files) {
      const filePath = join(dir, file);
      const fileStat = await stat(filePath);

      if (fileStat.isDirectory()) {
        images = images.concat(await getImagesRecursive(filePath));
      } else if (file.match(IMAGE_EXTENSIONS_REGEX) && !file.toLowerCase().includes("preview")) {
        const relativePath = relative("static", filePath);
        const imageUrl = `/${relativePath.replace(/\\/g, "/")}`;

        let exifData = {};
        try {
          const metadata = await parse(filePath, [
            "DateTimeOriginal",
            "GPSLatitude",
            "GPSLongitude"
          ]);

          if (metadata) {
            exifData = {
              date: metadata.DateTimeOriginal?.toISOString() || null,

              location:
                metadata.GPSLatitude && metadata.GPSLongitude
                  ? [metadata.GPSLatitude, metadata.GPSLongitude]
                  : null
            };
            console.log(`✅ EXIF extracted for ${file}`);
          } else {
            console.warn(`⚠️ No EXIF data found for ${file}`);
          }
        } catch (err) {
          console.warn(`⚠️ Could not read EXIF for ${file}: ${err.message}`);
        }

        images.push({
          url: imageUrl,
          name: file,
          ...exifData
        });
      }
    }
  } catch (error) {
    console.error(`❌ Error reading directory: ${dir}`, error);
  }

  return images;
}

async function generateNetlifyFunction() {
  try {
    const images = await getImagesRecursive(imageDir);

    const functionCode = `export async function handler() {
  return {
    statusCode: 200,
    headers: {
      "Content-Type": "application/json",
      "Access-Control-Allow-Origin": "*"
    },
    body: JSON.stringify(${JSON.stringify({ images }, null, 2)})
  };
}`;

    await writeFile(functionFile, functionCode);
    console.log(`✅ Netlify function created: ${functionFile}`);
  } catch (error) {
    console.error("❌ Error generating Netlify function:", error);
  }
}

generateNetlifyFunction();
