from __future__ import annotations

import numpy as np
import typing_extensions as tp
from functools import partial

from static_frame.core.index_base import IndexBase
from static_frame.core.util import JSONTranslator

if tp.TYPE_CHECKING:
    from static_frame.core.generic_aliases import TFrameAny
    TDtypeAny = np.dtype[tp.Any] # pylint: disable=W0611 #pragma: no cover

class NPYLabel:
    KEY_NAMES = '__names__'
    KEY_DEPTHS = '__depths__'
    KEY_TYPES = '__types__'
    KEY_TYPES_INDEX = '__types_index__'
    KEY_TYPES_COLUMNS = '__types_columns__'
    FILE_TEMPLATE_VALUES_INDEX = '__values_index_{}__.npy'
    FILE_TEMPLATE_VALUES_COLUMNS = '__values_columns_{}__.npy'
    FILE_TEMPLATE_BLOCKS = '__blocks_{}__.npy'


class JSONMeta:
    '''Metadata for JSON encodings.
    '''
    KEY_NAMES = NPYLabel.KEY_NAMES
    KEY_DEPTHS = NPYLabel.KEY_DEPTHS
    KEY_TYPES = NPYLabel.KEY_TYPES
    KEY_TYPES_INDEX = NPYLabel.KEY_TYPES_INDEX
    KEY_TYPES_COLUMNS = NPYLabel.KEY_TYPES_COLUMNS
    KEY_DTYPES = '__dtypes__'
    KEY_DTYPES_INDEX = '__dtypes_index__'
    KEY_DTYPES_COLUMNS = '__dtypes_columns__'

    @staticmethod
    def _dtype_to_str(dt: TDtypeAny) -> str:
        '''Normalize all dtype strings as platform native
        '''
        return '=' + dt.str[1:]

    @classmethod
    def _index_to_dtype_str(cls, index: IndexBase) -> tp.List[str]:
        if index.depth == 1:
            return [cls._dtype_to_str(index.dtype)] # type: ignore[attr-defined]
        return [cls._dtype_to_str(dt) for dt in index.dtypes.values] # type: ignore[attr-defined]

    @classmethod
    def to_dict(cls, f: TFrameAny) -> tp.Dict[str, tp.Any]:
        '''Generic routine to extract an JSON-encodable metadata bundle.
        '''
        # NOTE: need to store dtypes per index, per values; introduce new metadata label, use dtype.str to get string encoding

        md = {}
        md[cls.KEY_NAMES] = [
                JSONTranslator.encode_element(f._name),
                JSONTranslator.encode_element(f._index._name),
                JSONTranslator.encode_element(f._columns._name),
                ]

        md[cls.KEY_DTYPES] = [cls._dtype_to_str(dt) for dt in f.dtypes.values]
        md[cls.KEY_DTYPES_INDEX] = cls._index_to_dtype_str(f.index)
        md[cls.KEY_DTYPES_COLUMNS] = cls._index_to_dtype_str(f.columns)

        md[cls.KEY_TYPES] = [
                f._index.__class__.__name__,
                f._columns.__class__.__name__,
                ]

        for labels, key in (
                (f.index, cls.KEY_TYPES_INDEX),
                (f.columns, cls.KEY_TYPES_COLUMNS),
                ):
            if labels.depth > 1:
                md[key] = [cls.__name__ for cls in labels.index_types.values]

        md[cls.KEY_DEPTHS] = [
                len(f._blocks._blocks),
                f._index.depth,
                f._columns.depth]

        return md



    @staticmethod
    def _build_index_ctor(
            depth: int,
            cls_index: tp.Type['IndexBase'],
            name: TName,
            cls_components: tp.List[str],
            dtypes: tp.List[str],
            ):
        if depth == 1:
            return partial(cls_index, name=name, dtype=dtypes[0])

        from static_frame.core.index_hierarchy import IndexHierarchy

        return partial(IndexHierarchy.from_labels,
                name=name)


    @classmethod
    def from_dict_to_ctors(cls, md: tp.Dict[str, tp.Any]):

        names = metadata[NPYLabel.KEY_NAMES]
        name_index = JSONTranslator.decode_element(names[1])
        name_columns = JSONTranslator.decode_element(names[2])

        cls_index: tp.Type[IndexBase]
        cls_columns: tp.Type[IndexBase]
        cls_index, cls_columns = (ContainerMap.str_to_cls(n) # type: ignore
                for n in metadata[NPYLabel.KEY_TYPES])

        _, depth_index, depth_columns = metadata[NPYLabel.KEY_DEPTHS]

        index_ctor = cls._build_index_ctor(
                depth_index,
                cls_index,
                name_index,
                md[JSONMeta.KEY_TYPES_INDEX],
                md[JSONMeta.KEY_DTYPES_INDEX],
                )

        columns_ctor = cls._build_index_ctor(
                depth_columns,
                cls_columns,
                name_columns,
                md[JSONMeta.KEY_TYPES_COLUMNS],
                md[JSONMeta.KEY_DTYPES_COLUMNS],
                )

        return index_ctor, columns_ctor