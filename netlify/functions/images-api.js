exports.handler = async () => {
    const images = [
        { url: "/images/photo1.jpg", title: "Photo 1" },
        { url: "/images/photo2.jpg", title: "Photo 2" }
    ];
    return {
        statusCode: 200,
        body: JSON.stringify({ images }),
        headers: { "Content-Type": "application/json" }
    };
};
