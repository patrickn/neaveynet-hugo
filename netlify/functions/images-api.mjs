export async function handler() {
    const images = [
        { url: "/images/photo1.jpg", title: "Photo 1" },
        { url: "/images/photo2.jpg", title: "Photo 2" }
    ];

    return new Response(JSON.stringify({ images }), {
        status: 200,
        headers: { "Content-Type": "application/json" }
    });
}
