interface Props {
  label: string;
}

export default function Button({ label }: Props) {
  return (
    <a class="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline mr-2">
      {label}
    </a>
  );
}
