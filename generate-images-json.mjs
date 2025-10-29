import { readdir, writeFile, stat } from "fs/promises";
import { join, relative } from "path";

const imageDir = "static/img";
const functionDir = "netlify/functions";
const functionFile = join(functionDir, "image-api.mjs");

async function getImagesRecursive(dir) {
  let images = [];
  let exifr;

  // ✅ Properly import exifr and handle both default/named exports
  try {
    const exifrModule = await import("exifr");
    exifr = exifrModule.default || exifrModule;
  } catch {
    console.warn("⚠️ EXIF extraction skipped: 'exifr' package not found.");
  }

  try {
    const files = await readdir(dir);

    for (const file of files) {
      const filePath = join(dir, file);
      const fileStat = await stat(filePath);

      if (fileStat.isDirectory()) {
        images = images.concat(await getImagesRecursive(filePath));
      } else if (file.match(/\.(jpg|jpeg|png)$/i) && !file.toLowerCase().includes("preview")) {
        const relativePath = relative("static", filePath);
        const imageUrl = `/${relativePath.replace(/\\/g, "/")}`;

        let exifData = {};
        if (exifr) {
          try {
            const metadata = await exifr.parse(filePath, [
              "DateTimeOriginal",
              "GPSLatitude",
              "GPSLongitude"
            ]);

            if (metadata) {
              exifData = {
                date: metadata.DateTimeOriginal
                  ? metadata.DateTimeOriginal.toISOString()
                  : null,
                location:
                  metadata.GPSLatitude && metadata.GPSLongitude
                    ? {
                        lat: metadata.GPSLatitude,
                        lon: metadata.GPSLongitude
                      }
                    : null
              };
            }
          } catch (err) {
            console.warn(`⚠️ Could not read EXIF for ${file}: ${err.message}`);
          }
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
