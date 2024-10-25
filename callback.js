// api/callback.js
export default async function handler(req, res) {
  const { code } = req.query; // Spotify sends the code in the query parameters

  if (!code) {
    return res.status(400).send("Missing authorization code.");
  }

  // Exchange the authorization code for an access token
  const response = await fetch("https://accounts.spotify.com/api/token", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
      Authorization: `Basic ${Buffer.from(
        `${process.env.SPOTIFY_CLIENT_ID}:${process.env.SPOTIFY_CLIENT_SECRET}`
      ).toString("base64")}`,
    },
    body: new URLSearchParams({
      grant_type: "authorization_code",
      code,
      redirect_uri: process.env.REDIRECT_URI,
    }),
  });

  const data = await response.json();
  if (data.error) {
    return res.status(400).json(data);
  }

  res.status(200).json(data); // Send access token to the client
}
